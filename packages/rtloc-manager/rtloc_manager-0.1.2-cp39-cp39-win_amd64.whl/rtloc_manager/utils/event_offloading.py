"""
    RTLOC - Manager Lib

    rtloc_manager/utils/event_offloading.py

    (c) 2021 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>

"""

import time

from cx_packets import CXDWPacket

CTX_TASK_SD_EVENT_COUNT = 197

class EventOffloading:
    def __init__(self, listener):
        self.listener = listener

    def offload_events(self):
        self.listener.bind_tcp_socket()

        task_count = 0
        event_currently_offloading = {}
        event_offloading_waiting = {}
        event_start_dict = {}
        event_stop_dict = {}

        try:
            while True:
                    packets = self.listener.read_from_broadcast_socket()
                    for packet in packets:
                        # TODO FIX offloading of new live events that occur after initial offloading was completed
                        # TODO simplify, just keep track of the last offloaded sample for each device
                        if isinstance(packet, CXDWPacket):
                            # Ranging packages contain both info on the amount of events available
                            # as well as the actual events in a trailing child message
                            if packet.uwb_params.type == packet._MESSAGE_TYPE_RANGING:
                                # check which event was received, if any
                                received_events = packet.get_events()
                                received_event_nb = None
                                for event in received_events:
                                    # assuming that events are offloaded one by one
                                    received_event_nb = event.event_nr
                                    print("received event #{}".format(received_event_nb))
                                    print(event)

                                # check which events are available
                                events_start = packet.uwb_payload.events_start
                                events_stop = packet.uwb_payload.events_stop
                                # print("{} \t [EVENTS][START] {} [STOP] {}".format(packet.addr,
                                #                                                   events_start,
                                #                                                   events_stop))

                                # act on this events info
                                task_count += 1
                                amount = 1

                                # check whether we have an offloading history for the current device address
                                dest = packet.addr
                                try:
                                    event_currently_offloading[dest]
                                except KeyError:
                                    event_start_dict[dest] = events_start
                                    invalidate_until = events_start
                                    event_currently_offloading[dest] = 0
                                    event_offloading_waiting[dest] = 0
                                    event_stop_dict[dest] = events_stop

                                epoch = int(time.time())

                                if received_event_nb is not None and event_offloading_waiting != 0:
                                    try:
                                        assert received_event_nb == event_currently_offloading[dest]
                                    except AssertionError:
                                        event_currently_offloading[dest] = events_start
                                        assert received_event_nb == event_currently_offloading[dest]

                                    event_offloading_waiting[dest] = 0
                                    # until seems to be non-inclusive
                                    invalidate_until = received_event_nb + 1
                                    # overwrite start sample
                                    event_start_dict[dest] = received_event_nb + 1
                                    if event_start_dict[dest] > events_stop:
                                        print("-- acknowledging last event")
                                        message = self._create_event_offloading_task(dest, task_count, 0, 0, epoch, event_start_dict[dest])
                                        self.listener.write_to_tcp_socket(message)
                                elif events_stop > event_stop_dict[dest] and event_offloading_waiting[dest] == 0:
                                    # new data available
                                    print("{} -- NEW SAMPLES AVAILABLE".format(dest))
                                    event_start_dict[dest] = events_start #event_currently_offloading[dest] + 1
                                    invalidate_until = events_start #event_currently_offloading[dest] + 1
                                    event_stop_dict[dest] = events_stop
                                    # force offloading to happen
                                    event_currently_offloading[dest] = events_start - 1

                                if event_start_dict[dest] > events_stop:
                                    continue

                                # first time send for the current value of start sample
                                if event_start_dict[dest] > event_currently_offloading[dest]:
                                    print("{} \t sending offloading task - start {} amount {} invalidate {}".format(dest, event_start_dict[dest], amount, invalidate_until))
                                    message = self._create_event_offloading_task(dest, task_count, event_start_dict[dest], amount, epoch, invalidate_until)
                                    self.listener.write_to_tcp_socket(message)
                                    event_currently_offloading[dest] = event_start_dict[dest]
                                    event_offloading_waiting[dest] += 1
                                # periodic retry
                                elif event_offloading_waiting[dest] % 10 == 0 and event_offloading_waiting[dest] != 0:
                                    if event_offloading_waiting[dest] > 100:
                                        event_offloading_waiting[dest] = 0
                                        continue
                                    print("{} \t REsending offloading task - start {} amount {} invalidate {}".format(dest, event_currently_offloading[dest], amount, event_currently_offloading[dest]))
                                    message = self._create_event_offloading_task(dest, task_count, event_currently_offloading[dest], amount, epoch, event_currently_offloading[dest])
                                    self.listener.write_to_tcp_socket(message)
                                    event_offloading_waiting[dest] += 1
                                elif event_offloading_waiting[dest] != 0:
                                    event_offloading_waiting[dest] += 1

        except KeyboardInterrupt:
            self.listener.close_tcp_socket()

    @staticmethod
    def _create_event_offloading_task(dest, task_count, start_sample, amount, epoch, invalidate_until):
        # ctx_cmd
        packet = bytearray("@CX@", encoding="ascii")
        packet += bytearray("tk", encoding="ascii")
        packet += int(9 + 7 + 1 + 11).to_bytes(2, "little") # length
        packet += b'\x00'                                   # version

        packet += dest.to_bytes(2, "little")                # dest
        packet += int(7 + 1 + 11).to_bytes(2, "little")     # length
        packet += task_count.to_bytes(2, "little")          # task_cnt
        packet += b'\x00'                                   # task_repeat

        packet += int(CTX_TASK_SD_EVENT_COUNT).to_bytes(1, "little")

        packet += start_sample.to_bytes(2, "little")
        packet += amount.to_bytes(2, "little")
        packet += epoch.to_bytes(4, "little")
        packet += invalidate_until.to_bytes(2, "little")
        packet += bytearray("|", encoding="ascii")

        return packet
