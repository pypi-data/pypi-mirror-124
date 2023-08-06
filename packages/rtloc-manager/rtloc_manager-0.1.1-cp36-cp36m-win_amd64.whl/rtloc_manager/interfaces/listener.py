"""
    RTLOC - Manager Lib

    rtloc_manager/interfaces/listener.py

    (c) 2021 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>

"""

import socket

from cx_packets import CXDWPacket, CXHBPacket, TYPE_HB, TYPE_DW, RTLSChildMessage, Header
from rtloc_manager.manager_api import ManagerInterface, DistanceReport

RTLOC_TCP_PORT = 11800


class Listener:
    def __init__(self):
        self.fragmentation_buf = bytearray()
        self.broadcast_ip_addr = None

    """ 
    """
    def bind_broadcast_socket(self, port=11901):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Broadcast
        self.client.bind(("", port))

    def close_broadcast_socket(self):
        try:
            self.broadcast_ip_addr = None
            self.client.close()

        except AttributeError:
            # socket has not been binded
            # do nothing
            pass

    def read_from_broadcast_socket(self):
        # this socket call is blocking
        # TODO optimize buffer size
        recv_data, addr = self.client.recvfrom(4096)

        if self.broadcast_ip_addr != addr[0] and self.broadcast_ip_addr is not None:
            return []

        # UDP data can contain multiple cx packets
        multiple_cx_packets = True

        # fix for packet fragmentation
        # TODO: check whether this can be fixed using sockets lib
        recv_data = self.fragmentation_buf + recv_data
        self.fragmentation_buf = bytearray()

        packets = []

        while(multiple_cx_packets):
            try:
                header = Header(recv_data[:9])
            except UnicodeDecodeError:
                # can happen that the data is not of the expected format
                # print("[unexpected header data] clearing buffers and continuing")
                print("Decode Error")
                multiple_cx_packets = False
                self.fragmentation_buf = bytearray()
                continue
            except AssertionError:
                # TODO possibly the header is split, can we detect this?
                print("Assertion Error")
                multiple_cx_packets = False
                self.fragmentation_buf = bytearray()
                continue

            if len(recv_data) > header.packet_len:
                data = recv_data[:header.packet_len]
                recv_data = recv_data[header.packet_len:]
            else:
                data = recv_data
                multiple_cx_packets = False

            if len(data) != header.packet_len:
                self.fragmentation_buf = data
                continue

            assert len(data) == header.packet_len

            if header.type == TYPE_DW:
                packets.append(CXDWPacket(header, data))
                self.broadcast_ip_addr = addr[0]
            elif header.type == TYPE_HB:
                packets.append(CXHBPacket(header, data))

        return packets

    """ TCP socket related methods
    """
    def _discover_tcp_address(self):
        """ Discover TCP address from udp listener broadcast messages
        """
        while self.broadcast_ip_addr is None:
            # read from socket automatically sets the broadcast ip address
            self.read_from_broadcast_socket()

    def bind_tcp_socket(self):
        """ Bind TCP socket to the discovered listener address
        """
        self._discover_tcp_address()
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_client.connect((self.broadcast_ip_addr, RTLOC_TCP_PORT))

    def close_tcp_socket(self):
        """ Close TCP socket
        """
        self.tcp_client.close()

    def write_to_tcp_socket(self, message):
        """ Send given message over the TCP socket
        """
        self.tcp_client.send(message)


class AdhocListenerInterface(ManagerInterface):
    def __init__(self, port=11901, rate_reduction=False):
        self.listener = Listener()
        self.listener.bind_broadcast_socket(port=port)
        self.rate_reduction = rate_reduction
        if self.rate_reduction:
            self.addr_counters = {}

    def read_data(self):
        packets = self.listener.read_from_broadcast_socket()

        distance_reports = []

        for packet in packets:
            distances_dict = {}

            if packet.message_type != CXDWPacket._MESSAGE_TYPE_RANGING:
                continue

            for report in packet.reports:
                distances_dict[report.addr] = report.dist
    
            # rate reduction simulation
            if self.rate_reduction:
                try:
                    addr_count = self.addr_counters[packet.addr]
                except KeyError:
                    self.addr_counters[packet.addr] = 0
                    addr_count = 0

                if addr_count % 4 == 0:
                    distance_reports.append(DistanceReport(packet.addr, distances_dict))

                self.addr_counters[packet.addr] += 1

            else:
                distance_reports.append(DistanceReport(packet.addr, distances_dict))

        return distance_reports

    def stop(self):
        self.listener.close_broadcast_socket()

    def is_symmetrical(self):
        return True

class RTLSListenerInterface(ManagerInterface):
    def __init__(self):
        self.listener = Listener()
        self.listener.bind_broadcast_socket()

    def read_data(self):
        packets = self.listener.read_from_broadcast_socket()

        distance_reports = []

        for packet in packets:
            distances_dict = {}

            if packet.message_type != CXDWPacket._MESSAGE_TYPE_RTLS_TICK:
                continue

            for child_message in packet.child_messages:
                if child_message.type == RTLSChildMessage._MESSAGE_TYPE_REPORT:
                    for report in child_message.reports:
                        distances_dict[report.addr] = report.dist

                    distance_reports.append(DistanceReport(packet.addr, distances_dict))

        return distance_reports

    def stop(self):
        self.listener.close_broadcast_socket()

    def is_symmetrical(self):
        return False


import zmq
import json
import subprocess
import os

class CPPAdhocListenerInterface(ManagerInterface):
    def __init__(self, port=11901):
        # start cpp parser in background
        cpp_parser_exec = os.path.join(os.path.dirname(__file__), "../bin", "parser_exec.sh")
        self.parser_proc = subprocess.Popen([cpp_parser_exec, str(port)])

        self.context = zmq.Context()
        self.listener_socket = self.context.socket(zmq.SUB)
        self.listener_socket.connect("tcp://127.0.0.1:150720")
        self.listener_socket.setsockopt_string(zmq.SUBSCRIBE, "report")

    def read_data(self):
        msg = self.listener_socket.recv_multipart()
        reports = json.loads(msg[1])

        distance_reports = []
        for sender in reports.keys():
            tmp_dict = {}
            for addr in reports[sender].keys():
                # convert json to int
                tmp_dict[int(addr)] = int(reports[sender][addr])

            distance_reports.append(DistanceReport(int(sender), tmp_dict))

        return distance_reports

    def stop(self):
        self.parser_proc.kill()

    def is_symmetrical(self):
        return True
