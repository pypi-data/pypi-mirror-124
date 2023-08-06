"""
    RTLOC - Manager Lib

    rtloc_manager/database.py

    (c) 2020 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>

"""

import time
import math
import itertools

import numpy as np
import scipy.stats as ss
import scipy.linalg as la

from rtloc_manager.manager_api import DistanceReport, PositionReport
from rtloc_manager.core.engine import Position, DebugPostionEngine, PositionEngine


class ManagerDistanceDatabase:
    def __init__(self, manager_config, auto_calibration):
        # distance management
        self.distance_matrix = np.zeros((manager_config.nb_slots,
                                         manager_config.nb_slots))
        self.timing_matrix = np.zeros((self.distance_matrix.shape))

        # address management
        self.addresses = [0] * manager_config.nb_slots
        self.addresses_free = [True] * manager_config.nb_slots

        self.ignore_list = manager_config.ignore_list

        # filtering parameters
        self.inval_t = manager_config.dist_invalidate_delay
        self.alpha = manager_config.dist_smoothing_const

        # TODO make configurable
        self.anchors = manager_config.anchors
        self.tags = manager_config.tags

        try:
            self.anchor_height = manager_config.anchor_height
            self.tag_height = manager_config.tag_height

            print("[HEIGHT DIFFERENCE COMPENSATION] active")
            self.compensate_height_difference = True
        except AttributeError:
            self.compensate_height_difference = False
            print("[HEIGHT DIFFERENCE COMPENSATION] unactive")

        self.raw_init = False

        # initialize autocalibration
        self.auto_calibration = auto_calibration
        if self.auto_calibration:
            self._distance_corrections = {}
            self._anchor_positions = manager_config.anchor_positions

    def start_raw_init(self):
        # create temporary data structure for storing raw distances
        self.distance_tensor = np.empty(self.distance_matrix.shape, dtype=np.object)
        self.raw_init = True

    def _append_raw_init(self, raw_distance, row_slot, column_slot):
        if self.distance_tensor[row_slot, column_slot] is None:
            self.distance_tensor[row_slot, column_slot] = []

        self.distance_tensor[row_slot, column_slot].append(raw_distance)

    def stop_raw_init(self):
        self.raw_init = False

        for row_idx, row_free in enumerate(self.addresses_free):
            if row_free:
                continue

            row_address = self.addresses[row_idx]

            for col_idx, col_free in enumerate(self.addresses_free):
                if col_free or row_idx == col_idx:
                    continue

                col_address = self.addresses[col_idx]

                distance = self._filter_distance_raw_init(row_idx, col_idx)
                self.update_distance(row_address, col_address, distance, force_overwrite=True)

        self.distance_tensor = None

        if self.auto_calibration:
            self._run_auto_calibration()

    def _run_auto_calibration(self):
        nb_anchors = len(self.anchors)
        pairs = itertools.combinations(range(nb_anchors), 2)
        nb_pairs = sum(1 for _ in pairs)
        # reset iterator
        pairs = itertools.combinations(range(nb_anchors), 2)

        A = np.zeros((nb_pairs, nb_anchors))
        b = np.zeros((nb_pairs, 1))

        # populate A and b
        for row_idx, anchor_idxs in enumerate(pairs):
            # A
            A[row_idx, anchor_idxs] = 1

            # b
            first_anchor = self.anchors[anchor_idxs[0]]
            second_anchor = self.anchors[anchor_idxs[1]]

            report_first = self.get_distance_report(first_anchor)
            report_second = self.get_distance_report(second_anchor)

            d_est_fs = report_first.distances_dict[second_anchor]
            d_est_sf = report_second.distances_dict[first_anchor]

            coord_first = self._anchor_positions[first_anchor]
            coord_second = self._anchor_positions[second_anchor]

            d_coord = math.sqrt((coord_first[0]-coord_second[0])**2 + (coord_first[1]-coord_second[1])**2)

            b[row_idx] = d_est_fs + d_est_sf - 2 * d_coord

        # compute corrections
        corrections = la.lstsq(A, b)[0]
        corrections = corrections.flatten()

        for anchor_idx, correction in enumerate(corrections):
            self._distance_corrections[self.anchors[anchor_idx]] = correction / 2

    def _get_distance_correction(self, id):
        return self._distance_corrections.get(id, 0)

    def _filter_distance_raw_init(self, row_idx, col_idx):
        distances = self.distance_tensor[row_idx, col_idx]
        if distances is None:
            raise ValueError("Raw init error: no distances were found for the given row and column indices: {}, {}".format(row_idx, col_idx))

        distances = np.array(distances)

        # outlier rejection
        med = np.median(distances)
        mad = ss.median_abs_deviation(distances)
        mask = (distances >= (med - 3 * mad)) & (distances <= (med + 3 * mad))

        distances = distances[mask]

        if distances.size == 0:
            raise ValueError("Raw init error: no distances remaing after outlier rejection")

        return distances.mean()

    def set_interface_symmetrical(self, interface_symmetrical):
        self.interface_symmetrical = interface_symmetrical

    def update_distance(self, device_id, remote_device_id, distance, force_overwrite=False):
        """ Dual filtering (smoothing and symmetrical averaging) distance update
        """
        if not self._is_address_valid(device_id) or not self._is_address_valid(remote_device_id):
            # don't update for invalid address
            return

        if not self._is_distance_valid(distance):
            return

        dev_slot = self._get_address_slot(device_id)
        remote_dev_slot = self._get_address_slot(remote_device_id)

        # Pythagorean compensation
        if self.compensate_height_difference:
            # only compensate for pair of anchor and tag
            compensation_needed = (device_id in self.tags and remote_device_id in self.anchors) or\
                                  (device_id in self.anchors and remote_device_id in self.tags)

            if compensation_needed:
                distance = self._compensate_height_difference(distance)

        if self.raw_init:
            self._append_raw_init(distance, dev_slot, remote_dev_slot)

        if not force_overwrite:
            # SMOOTHING
            filt_distance = (1 - self.alpha) * self.distance_matrix[dev_slot, remote_dev_slot] + self.alpha * distance

            # SYMMETRICAL AVERAGING
            if self.interface_symmetrical:
                # incorporate far end distance knowledge
                filt_distance += self.distance_matrix[remote_dev_slot, dev_slot]
                filt_distance /= 2

            # update internal representation
            self._update_distance(dev_slot, remote_dev_slot, filt_distance)

            if self.interface_symmetrical:
                # don't update time for the symmetrical update, because this is not based on own measurements
                self._update_distance(remote_dev_slot, dev_slot, filt_distance, update_time=False)
            else:
                # in the assymetrical case, the device completely manages the remote slot as well
                self._update_distance(remote_dev_slot, dev_slot, filt_distance)
        else:
            # force given distance overwrite, no smoothing or mirroring applied
            self._update_distance(dev_slot, remote_dev_slot, distance)

    def _update_distance(self, row_slot, column_slot, dist, update_time=True):
        self.distance_matrix[row_slot, column_slot] = dist
        if update_time:
            self.timing_matrix[row_slot, column_slot] = time.time()

    def update_from_report(self, report):
        """ Update internal representation from a distance report based on
        the update_distance method.
        """
        device_id = report.device_id

        # iterate over dictionary keys
        for remote_device_id in report.distances_dict:
            self.update_distance(device_id, remote_device_id,
                                 report.distances_dict[remote_device_id])

        # prune old distances from database
        self.invalidate()

    def get_distance_report(self, device_id):
        """ Return the distance report for the given device_id
        """
        distances_dict = {}

        if not self._is_address_valid(device_id):
            # return empty dict for invalid address
            return None

        row_slot = self._get_address_slot(device_id)

        # add self distance
        distances_dict[device_id] = 0

        for remote_device_id in self.addresses:
            if self._is_address_valid(remote_device_id):
                column_slot = self._get_address_slot(remote_device_id)

                if self.auto_calibration:
                    distances_dict[remote_device_id] = self.distance_matrix[row_slot, column_slot]\
                        - self._get_distance_correction(device_id)\
                        - self._get_distance_correction(remote_device_id)
                else:
                    distances_dict[remote_device_id] = self.distance_matrix[row_slot, column_slot]

        return DistanceReport(device_id, distances_dict)

    def get_all_distance_reports(self):
        """ Return a list of all distance reports present in the internal
        database.
        """
        reports = []

        for slot, free in enumerate(self.addresses_free):
            if not free:
                device_id = self.addresses[slot]
                reports.append(self.get_distance_report(device_id))

        return reports

    def invalidate(self):
        """ Invalidate distances that have not been received recently
        """
        self.distance_matrix[self.timing_matrix < (time.time() - self.inval_t)] = 0
        self._free_invalidated_address_slots()

    def _is_distance_valid(self, dist):
        if dist == 0 or dist == 65534:
            return False
        else:
            return True

    def _is_address_valid(self, address):
        if address == 0 or address == 255 or address in self.ignore_list:
            return False
        else:
            return True

    def _get_address_slot(self, address):
        try:
            slot = self.addresses.index(address)
        except ValueError:
            slot = self._assign_address_slot(address)

        return slot

    def _assign_address_slot(self, address):
        try:
            slot = self.addresses_free.index(True)
        except ValueError:
            raise NoFreeAddressSlotError

        # assign slot to given address
        self.addresses[slot] = address
        self.addresses_free[slot] = False

        return slot

    def _free_invalidated_address_slots(self):
        for slot, free in enumerate(self.addresses_free):
            if not free:
                if np.sum(self.distance_matrix[slot,:]) == 0:
                    # print("Device {} is invalidated".format(self.addresses[slot]))
                    self.addresses[slot] = 0
                    self.addresses_free[slot] = True

    def _compensate_height_difference(self, dist):
        compensated_dist = dist**2 - (self.anchor_height - self.tag_height)**2
        if compensated_dist < 1:
            return 1

        return math.sqrt(compensated_dist)


class ManagerPositionDatabase:
    NB_ANCHORS_USED_PER_POSITION = 3

    def __init__(self, manager_config):
        # copy anchor and tag IDs
        self.anchors = manager_config.anchors
        self.tags = manager_config.tags
        # TODO experimental
        self.anchor_corrections = [0] * len(self.anchors)

        self.alpha = manager_config.pos_smoothing_const

        # position dict to keep positions of both anchors and tags
        self.position_dict = {}

        # set anchor positions if given (if not all given, the given ones will be overwritten
        # by the auto positioning procedure).
        for anchor in self.anchors:
            try:
                self.position_dict[anchor] =  Position(*manager_config.anchor_positions[anchor])
            except (KeyError, TypeError):
                # anchor position not known
                pass

        # init tag position to abritrary value
        for tag in self.tags:
            self.position_dict[tag] = Position(0, 0, 0)

        # position engine
        self.engine = DebugPostionEngine(self.NB_ANCHORS_USED_PER_POSITION)
        # self.engine = PositionEngine(self.NB_ANCHORS_USED_PER_POSITION)

    def anchor_positions_known(self):
        """ Return whether or not all anchor positions are known.
        """
        for anchor in self.anchors:
            if self.get_device_position(anchor) is None:
                return False

        # all position are in the position dict
        return True

    def get_device_position(self, device_id):
        """ Returns position for the given device if known.
        Otherwise returns None.
        """
        try:
            return self.position_dict[device_id]
        except KeyError:
            return None

    def set_device_position(self, device_id, position):
        """ Set the position of given device based on the given
        Position object.
        """
        self.position_dict[device_id] = position

    def feed_anchor_positions_to_engine(self, anchors):
        positions = [self.get_device_position(anchor) for anchor in anchors]
        self.engine.set_anchor_positions(positions)

    def update_tag_position_from_report(self, ranging_report):
        if ranging_report.device_id not in self.tags:
            # this tag is device is not to be tracked
            return

        previous_tag_position = self.get_device_position(ranging_report.device_id)

        # assume not all anchors are within measurement reach
        measurements = []
        reachable_anchors = []
        for anchor in self.anchors:
            try:
                measurements.append(ranging_report.distances_dict[anchor])
                reachable_anchors.append(anchor)
            except KeyError:
                pass

        if len(reachable_anchors) < self.NB_ANCHORS_USED_PER_POSITION:
            raise NotEnoughAnchorMeasurements

        # # select the NB_ANCHORS_USED_PER_POSITION furthest anchors for positioning
        # sorted_idxs = np.argsort(measurements)[::-1]

        measurements_idxs = range(len(measurements))

        # sse = None
        new_tag_position = Position(0, 0, 0)

        weights_sum = 0

        for subset_idxs in itertools.combinations(measurements_idxs, self.NB_ANCHORS_USED_PER_POSITION):
            subset_idxs = np.array(subset_idxs)
            # TODO: reject sets of measurement based on lower and upper bound
            measurements_slice = np.array(measurements)[subset_idxs[:self.NB_ANCHORS_USED_PER_POSITION]].tolist()
            anchors_slice = np.array(reachable_anchors)[subset_idxs[:self.NB_ANCHORS_USED_PER_POSITION]].tolist()

            # # skip sets that contain measurements smaller than 20 cm
            # if np.any(np.array(measurements_slice) < 20):
            #     continue

            self.feed_anchor_positions_to_engine(anchors_slice)
            # TODO experimental
            previous_tag_position.corrections = np.array(self.anchor_corrections)[subset_idxs[:self.NB_ANCHORS_USED_PER_POSITION]].tolist()

            tmp_tag_position = self.engine.compute_tag_position(measurements_slice, previous_tag_position)
            # TODO experimental
            for order_idx, subset_idx in enumerate(subset_idxs):
                self.anchor_corrections[subset_idx] = tmp_tag_position.corrections[order_idx]

            weight = 1 / math.sqrt(self.engine.get_sse())
            new_tag_position.x += weight * tmp_tag_position.x
            new_tag_position.y += weight * tmp_tag_position.y
            new_tag_position.z += weight * tmp_tag_position.z

            weights_sum += weight

            # if sse is None:
            #     sse = self.engine.get_sse()
            #     new_tag_position = tmp_tag_position
            # elif self.engine.get_sse() < sse:
            #     sse = self.engine.get_sse()
            #     new_tag_position = tmp_tag_position

        if weights_sum == 0:
            print("Position not updated.")
            return

        # perform position smoothing
        new_tag_position.x = (1 - self.alpha) * previous_tag_position.x + self.alpha * (new_tag_position.x / weights_sum)
        new_tag_position.y = (1 - self.alpha) * previous_tag_position.y + self.alpha * (new_tag_position.y / weights_sum)
        new_tag_position.z = (1 - self.alpha) * previous_tag_position.z + self.alpha * (new_tag_position.z / weights_sum)

        self.set_device_position(ranging_report.device_id, new_tag_position)
        # print("corrections:", self.anchor_corrections)

    def get_position_report(self, device_id):
        return PositionReport(device_id, self.get_device_position(device_id))


""" Custom exceptions
"""
class NoFreeAddressSlotError(Exception):
    pass

class NotEnoughAnchorMeasurements(Exception):
    pass
