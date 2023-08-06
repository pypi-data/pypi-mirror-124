"""
    RTLOC - Manager Lib

    rtloc_manager/utils/firmware_update.py

    (c) 2021 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>

"""

import time
import crc16
import math

from cx_packets import CXDWPacket

FW_CHUNK_SIZE = 128

class FirmwareUpdate:
    def __init__(self, listener):
        self.listener = listener

    def firmware_update(self, image, target):
        self.listener.bind_tcp_socket()

        with open(image, "rb") as fh:
            binary_image = fh.read()

        # binary_image = binary_image[:int(100*FW_CHUNK_SIZE)]

        nb_parts = math.ceil(len(binary_image) / FW_CHUNK_SIZE)
        pad_len = FW_CHUNK_SIZE - (len(binary_image) % FW_CHUNK_SIZE)
        if pad_len < FW_CHUNK_SIZE:
            binary_image += (b'\x00' * pad_len)

        print("[IMAGE SIZE INCLUDING PADDING] {}".format(len(binary_image)))

        crc_tot = crc16.crc16xmodem(binary_image, 0xFFFF)

        task_count = 0

        task_count += 1
        # force update
        packet = self._create_fw_update_force_task(task_count, len(binary_image))
        self.listener.write_to_tcp_socket(packet)
        time.sleep(1)

        # part_nb = 0
        # part_nb = 1
        for part_nb in range(nb_parts):
            part_nb += 1
            print("[FW UPDATE] sending part {} of {}".format(part_nb, nb_parts))

            task_count += 1

            if part_nb == 0:
                data = b'\x00' * FW_CHUNK_SIZE
            else:
                data = binary_image[int((part_nb-1)*FW_CHUNK_SIZE):int((part_nb)*FW_CHUNK_SIZE)]

            if len(data) < FW_CHUNK_SIZE:
                data += (b'\x00' * (FW_CHUNK_SIZE - len(data)))

            # packet = self._create_fw_update_packet(part_nb, nb_parts, data, crc_tot, len(binary_image), target)
            packet = self._create_fw_update_task_chunk(part_nb, nb_parts, data, crc_tot, len(binary_image), target, task_count)

            # send packet over tcp
            self.listener.write_to_tcp_socket(packet)

            time.sleep(0.2)

            part_nb += 1

            if part_nb > nb_parts:
                part_nb = 1

            # fwup_found = False
            # while not fwup_found:
            #     packets = self.read_from_broadcast_socket()
            #     for packet in packets:
            #         # until a heartbeat packet is found
            #         if isinstance(packet, CXDWPacket):
            #             if packet.uwb_params.type == packet._MESSAGE_TYPE_FWUP_STATUS:
            #                 fwup_found = True
            #                 print("[PART MISSING] {}".format(packet.uwb_payload.parts_missing))
            #                 break

        # send out missed packets
        while True:
            self.listener.close_broadcast_socket()
            self.listener.bind_broadcast_socket()
            fwup_found = False
            while not fwup_found:
                packets = self.listener.read_from_broadcast_socket()
                for packet in packets:
                    # until a heartbeat packet is found
                    if isinstance(packet, CXDWPacket):
                        if packet.uwb_params.type == packet._MESSAGE_TYPE_FWUP_STATUS:
                            fwup_found = True
                            break

            print("[PART MISSING] {}".format(packet.uwb_payload.parts_missing))
            print(packet.uwb_payload.bitmap)

            # TODO we should check that the parts missing is coming
            # from the device we are updating (important for when multiple tags are being updated simultaneously)
            if packet.uwb_payload.parts_missing == 0:
                break

            bitmap = packet.uwb_payload.bitmap
            for byte_nb in range(math.ceil(nb_parts / 8)):
                for bit_idx in range(8):
                    part_nb = bit_idx + 8 * byte_nb + 1
                    if part_nb > nb_parts:
                        continue

                    if (bitmap[byte_nb] >> bit_idx) & 0x01 == 0:
                        task_count += 1

                        data = binary_image[int((part_nb-1)*FW_CHUNK_SIZE):int((part_nb)*FW_CHUNK_SIZE)]
                        packet = self._create_fw_update_task_chunk(part_nb, nb_parts, data, crc_tot, len(binary_image), target, task_count)
                        self.listener.write_to_tcp_socket(packet)
                        time.sleep(0.2)

            ## receive packet over tcp
            # while True:
            #     response = self.tcp_client.recv(1024)

            #     if response[:6] == bytearray("@CX@UL", encoding="ascii"):
            #         break

            # part_nb = int.from_bytes(response[10:12], "little")
            # print("[RESPONSE] {}".format(part_nb))
            # # check if upload is finished
            # if part_nb == 0xFFFF:
            #     break

        # close tcp socket
        self.listener.close_tcp_socket()

    @staticmethod
    def _create_fw_update_packet(part_nb, nb_parts, data, crc_tot, size_tot, target):
        # ctx_cmd
        packet = bytearray("@CX@", encoding="ascii")
        packet += bytearray("ul", encoding="ascii")
        packet += int(9 + 19 + len(data)).to_bytes(2, "little")     # length
        packet += b'\x00'                                           # version

        # msg_file
        packet += target                                    # target
        packet += b'\x00\x00'                               # version
        packet += crc_tot.to_bytes(2, "little")             # crc_tot
        packet += int(size_tot).to_bytes(4, "little")       # size

        packet += part_nb.to_bytes(2, "little")
        packet += nb_parts.to_bytes(2, "little")
        packet += len(data).to_bytes(2, "little")
        packet += crc16.crc16xmodem(data, 0xFFFF).to_bytes(2, "little")

        packet += b'\x00'   # hw_version
        packet += b'\x00'   # desc_flag

        packet += data

        return packet

    @staticmethod
    def _create_fw_update_force_task(task_count, size_tot):
        # ctx_cmd
        packet = bytearray("@CX@", encoding="ascii")
        packet += bytearray("tk", encoding="ascii")
        packet += int(9 + 7 + 9).to_bytes(2, "little")      # length
        packet += b'\x00'                                   # version

        packet += b'\x1D\x00'                               # dest
        packet += int(7 + 9).to_bytes(2, "little")          # length
        packet += task_count.to_bytes(2, "little")          # task_cnt
        packet += b'\x00'                                   # task_repeat

        # task type
        packet += int(211).to_bytes(1, "little")

        packet += b'\x07'                                   # type
        # TODO extract version from binary
        packet += b'\x00\x00'                               # version
        packet += b'\x00'                                   # subversion
        packet += int(size_tot).to_bytes(4, "little")       # file length
        packet += bytearray("|", encoding="ascii")          # eoh

        return packet

    @staticmethod
    def _create_fw_update_task_chunk(part_nb, nb_parts, data, crc_tot, size_tot, target, task_count):
        # ctx_cmd
        packet = bytearray("@CX@", encoding="ascii")
        packet += bytearray("tk", encoding="ascii")
        packet += int(9 + 7 + 1 + len(data)).to_bytes(2, "little")  # length
        packet += b'\x00'                                           # version

        packet += b'\x07\x00'                                       # dest
        packet += int(7 + 9 + 1 + len(data)).to_bytes(2, "little")  # length
        packet += task_count.to_bytes(2, "little")                  # task_cnt
        packet += b'\x00'                                           # task_repeat

        # task type
        packet += int(209).to_bytes(1, "little")            # type\

        packet += target                                    # target
        packet += b'\x00\x00'                               # version
        packet += crc_tot.to_bytes(2, "little")             # crc_tot
        packet += int(size_tot).to_bytes(4, "little")       # size

        packet += part_nb.to_bytes(2, "little")
        packet += nb_parts.to_bytes(2, "little")
        packet += len(data).to_bytes(2, "little")
        packet += crc16.crc16xmodem(data, 0xFFFF).to_bytes(2, "little")

        packet += b'\x00'   # hw_version
        packet += b'\x00'   # desc_flag

        packet += data

        return packet
