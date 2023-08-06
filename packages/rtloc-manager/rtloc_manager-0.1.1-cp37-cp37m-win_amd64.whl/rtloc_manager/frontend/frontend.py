"""
    RTLOC - Manager Lib

    rtloc_manager/frontend/frontend.py

    (c) 2021 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>

"""

import os
import sys
import time
import threading
import asyncio
import math

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2.QtCore import Signal, QTimer, QThreadPool
import qdarkstyle

from rtloc_manager.frontend.ui import rtloc
from rtloc_manager.manager_api import ManagerPositionApp, ManagerDistanceApp
from rtloc_manager.frontend.workers import AlarmToggleWorker

import pyqtgraph as pg

class _PositionGUI(QtWidgets.QMainWindow, rtloc.Ui_RTLOC):
    data_ready = Signal(int, list, list)
    debug_data_ready = Signal(int, int)

    def __init__(self, config, parent=None):
        # boiler plate
        super().__init__(parent)
        self.setupUi(self)

        self.plotting_data = {}
        self.tag_position_last_updated = {}

        # initialize custom GUI elements
        self.create_plotting_area()
        self.data_ready.connect(self.update_plot)
        self.debug_data_ready.connect(self.update_debug_plot)

        # cleanup timer
        self.cleanup_timer = QTimer()
        self.cleanup_timer.timeout.connect(self.cleanup_tags)
        self.cleanup_timer.start(1000)

        self.selected_device_id = None
        self.threadpool = QThreadPool()

        self.btn_toggle_alarm.clicked.connect(self.btn_toggle_alarm_clicked)

        self.silence_group_id = None
        self.btn_toggle_alarm.setVisible(False)

        self.anchors = config.anchors
        self.tags = config.tags

    def _spin_async_event_loop(self):
        asyncio.set_event_loop(self.async_event_loop)
        self.async_event_loop.run_forever()

    def set_silence_group_id(self, silence_group_id):
        self.silence_group_id = silence_group_id
        self.btn_toggle_alarm.setVisible(True)

        # create custom async io loop which is needed to use the ble interface
        self.async_event_loop = asyncio.new_event_loop()
        threading.Thread(target=self._spin_async_event_loop, daemon=True).start()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

        event.accept()

    def create_plotting_area(self):
        # create plotting canvas
        self.plotting_area = pg.PlotWidget()

        self.plotting_area.setAspectLocked()

        self.plotting_area.setBackground(background=(25, 35, 45))
        self.plotting_area.setLabel("left", text="Y distance [cm]")
        self.plotting_area.setLabel("bottom", text="X distance [cm]")

        # set size policy for the plot object
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Expanding)
        self.plotting_area.setSizePolicy(sizePolicy)

        # add canvas widget to UI
        self.plotGrid.addWidget(self.plotting_area)

    def create_forklift_overlay(self):
        self.plotting_area.setXRange(-600, 600, padding=0)
        self.plotting_area.setYRange(-600, 600, padding=0)

        warning_circle = pg.QtGui.QGraphicsEllipseItem(-500, -500, 1000, 1000)
        warning_circle.setPen(pg.mkPen(237, 185, 94))
        warning_circle.setBrush(pg.mkBrush(237, 185, 94))

        self.plotting_area.addItem(warning_circle)

        danger_circle = pg.QtGui.QGraphicsEllipseItem(-250, -250, 500, 500)
        danger_circle.setPen(pg.mkPen(226, 54, 54))
        danger_circle.setBrush(pg.mkBrush(226, 54, 54))

        self.plotting_area.addItem(danger_circle)

        dirname = os.path.dirname(__file__)
        forklift_fn = os.path.join(dirname, "img/forklift.png")
        print(forklift_fn)
        forklift = pg.QtGui.QGraphicsPixmapItem(pg.QtGui.QPixmap(forklift_fn))
        self.plotting_area.addItem(forklift)

        # scale
        forklift_w = forklift.boundingRect().width()
        forklift_true_w = 115 # in cm
        forklift_scaling = forklift_true_w / forklift_w
        forklift.scale(forklift_scaling, -forklift_scaling)

        # translate
        forklift_h = forklift.boundingRect().height()
        forklift_w = forklift.boundingRect().width()

        forklift.translate(-forklift_w/2, -forklift_h/2)

    def create_plotting_data(self, device_id, cleanup=False, **kwargs):
        """ Create a plotting data object for the given device id
        """
        self.plotting_data[device_id] = pg.ScatterPlotItem(**kwargs)
        self.plotting_data[device_id].setData([1], [1])
        self.plotting_area.addItem(self.plotting_data[device_id])

        # add anchor address in plot
        self.plotting_data[str(device_id) + "_text"] = pg.TextItem(str(device_id))
        self.plotting_data[str(device_id) + "_text"].setPos(1, 1)
        self.plotting_area.addItem(self.plotting_data[str(device_id) + "_text"])

        # connect click listener
        self.plotting_data[device_id].sigClicked.connect(self.clicked)

        if cleanup:
            self.tag_position_last_updated[device_id] = time.time()

    def create_debug_line(self, device_id):
        self.plotting_data[str(device_id) + "_line"] = pg.PlotCurveItem()
        self.plotting_data[str(device_id) + "_line"].setData([1, 1], [1, 1])
        self.plotting_area.addItem(self.plotting_data[str(device_id) + "_line"])

        self.plotting_data[str(device_id) + "_line_text"] = pg.TextItem()
        self.plotting_data[str(device_id) + "_line_text"].setPos(1, 1)
        self.plotting_area.addItem(self.plotting_data[str(device_id) + "_line_text"])

    def clicked(self, obj, pts, evt):
        for device_id in self.tag_position_last_updated.keys():
            if (self.plotting_data[device_id] is obj):
                self.selected_device_id = device_id
                self.paint_btn_toggle_alarm()

    def paint_btn_toggle_alarm(self):
        btn_label = "Toggle alarm "
        btn_label += self._get_ble_device_name()
        self.btn_toggle_alarm.setText(btn_label)

        if self.selected_device_id is None:
            self.btn_toggle_alarm.setEnabled(False)
        else:
            self.btn_toggle_alarm.setEnabled(True)

    def _get_ble_device_name(self):
        device_prefix = "DIS"
        if self.selected_device_id is None:
            return device_prefix + "XXXX"
        else:
            device_id = str(self.selected_device_id)
            padding = 4 - len(device_id)
            if padding > 0:
                device_prefix += "0" * padding

            return device_prefix + device_id

    def btn_toggle_alarm_clicked(self):
        if self.silence_group_id is None:
            print("Unexpected issue: silence group id is not set")
            return

        self.ble_worker = AlarmToggleWorker(self.silence_group_id)
        self.ble_worker.set_device_name(self._get_ble_device_name())
        self.ble_worker.set_event_loop(self.async_event_loop)
        self.threadpool.start(self.ble_worker)

    def get_plotting_data(self, plotting_data_key):
        return self.plotting_data[plotting_data_key]

    def update_plot(self, device_id, x, y):
        plotting_data = self.get_plotting_data(device_id)
        plotting_data.setData(x, y)

        plotting_data = self.get_plotting_data(str(device_id) + "_text")
        plotting_data.setPos(x[-1], y[-1])

        if device_id in self.tag_position_last_updated.keys():
            self.tag_position_last_updated[device_id] = time.time()

        if device_id in self.anchors:
            plotting_data = self.get_plotting_data(str(device_id) + "_line")

            x_tmp = plotting_data.xData
            x_tmp[0] = x[0]

            y_tmp = plotting_data.yData
            y_tmp[0] = y[0]

            plotting_data.setData(x_tmp, y_tmp)
        else:
            # debug lines only for first tag
            if device_id == self.tags[0]:
                for anchor in self.anchors:
                    plotting_data = self.get_plotting_data(str(anchor) + "_line")

                    x_tmp = plotting_data.xData
                    x_tmp[1] = x[-1]

                    y_tmp = plotting_data.yData
                    y_tmp[1] = y[-1]

                    plotting_data.setData(x_tmp, y_tmp)

    def update_debug_plot(self, device_id, distance):
        line = self.get_plotting_data(str(device_id) + "_line")
        x = (line.xData[0] + line.xData[1]) / 2
        y = (line.yData[0] + line.yData[1]) / 2

        # estimated difference based on position
        if distance != "":
            data_anchor = self.get_plotting_data(device_id)
            data_tag = self.get_plotting_data(self.tags[0])
            est_dist = math.sqrt((data_anchor.data['x'][-1] - data_tag.data['x'][-1])**2 + (data_anchor.data['y'][-1] - data_tag.data['y'][-1])**2)
            diff_dist = int(distance) - int(est_dist)
        else:
            diff_dist = ""

        text = self.get_plotting_data(str(device_id) + "_line_text")
        text.setText(str(distance) + " ({})".format(diff_dist))
        text.setPos(x, y)

    def cleanup_tags(self, max_outdated_sec=3):
        now = time.time()
        for device_id in self.tag_position_last_updated.keys():
            if (now - self.tag_position_last_updated[device_id]) > max_outdated_sec:
                self.get_plotting_data(device_id).setVisible(False)
                self.get_plotting_data(str(device_id) + "_text").setVisible(False)
            else:
                self.get_plotting_data(device_id).setVisible(True)
                self.get_plotting_data(str(device_id) + "_text").setVisible(True)

        self.cleanup_timer.start(1000)


class ManagerFrontend:
    def __init__(self, config, forklift_demo=False, silence_group_id=None):
        super().__init__()

        self.anchors = config.anchors
        self.tags = config.tags

        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

        self.ui = _PositionGUI(config)
        if forklift_demo:
            self.ui.create_forklift_overlay()
        if silence_group_id is not None:
            self.ui.set_silence_group_id(silence_group_id)

        # init plotting data
        for device in config.tags + config.anchors:
            if device in config.tags:
                self.ui.create_plotting_data(device, pen=pg.mkPen(width=10, color="g"), symbol="o", cleanup=True)
            else:
                self.ui.create_plotting_data(device, pen=pg.mkPen(width=10, color=(226, 54, 54)), symbol="+")
                self.ui.create_debug_line(device)

    def event_loop(self):
        self.ui.show()
        self.app.exec_()

    def get_data_ready_signal(self):
        return self.ui.data_ready

    def get_debug_data_ready_signal(self):
        return self.ui.debug_data_ready



class PositionGUIPlotter(ManagerPositionApp):
    X = 0
    Y = 1

    def __init__(self, config):
        super().__init__()

        self.tags = config.tags
        self.anchors = config.anchors

        self.local_plotting_data = {}

        for device in config.tags + config.anchors:
            self.local_plotting_data[device] = {self.X: [], self.Y: []}

    def run(self):
        while True:
            position_report = self.pop_report()

            if position_report.device_id in self.anchors:
                self.plot_anchor_position(position_report)

            if position_report.device_id in self.tags:
                self.plot_tag_position(position_report)

    def set_data_ready_signal(self, data_ready_signal):
        self.data_ready_signal = data_ready_signal

    def plot_anchor_position(self, position_report):
        self.plot_tag_position(position_report)

    def plot_tag_position(self, position_report):
        dev_id = position_report.device_id

        # self.local_plotting_data[dev_id][self.X] = self.local_plotting_data[dev_id][self.X][-4:]
        self.local_plotting_data[dev_id][self.X] = self.local_plotting_data[dev_id][self.X][-1:]
        self.local_plotting_data[dev_id][self.X].append(position_report.position.x)

        # self.local_plotting_data[dev_id][self.Y] = self.local_plotting_data[dev_id][self.Y][-4:]
        self.local_plotting_data[dev_id][self.Y] = self.local_plotting_data[dev_id][self.Y][-1:]
        self.local_plotting_data[dev_id][self.Y].append(position_report.position.y)

        # actually change data, that will get plotted by the event loop
        self.data_ready_signal.emit(dev_id, self.local_plotting_data[dev_id][self.X], self.local_plotting_data[dev_id][self.Y])


class DebugDistanceGUIPlotter(ManagerDistanceApp):
    def __init__(self, config):
        super().__init__()

        self.tags = config.tags
        self.anchors = config.anchors

    def run(self):
        while True:
            distance_report = self.pop_report()

            if distance_report.device_id in self.tags:
                self.update_debug_distance(distance_report)

    def set_data_ready_signal(self, data_ready_signal):
        self.data_ready_signal = data_ready_signal

    def update_debug_distance(self, distance_report):
        # only draw debug lines for the first tag
        if distance_report.device_id == self.tags[0]:
            remote_dev_ids = list(distance_report.distances_dict.keys())

            for anchor in self.anchors:
                if anchor in remote_dev_ids:
                    self.data_ready_signal.emit(anchor, distance_report.distances_dict[anchor])
                else:
                    self.data_ready_signal.emit(anchor, "")
