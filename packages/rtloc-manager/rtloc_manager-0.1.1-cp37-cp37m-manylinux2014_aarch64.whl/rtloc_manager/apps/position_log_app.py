"""
    RTLOC - Manager Lib

    rtloc_manager/apps/position_log_app.py

    (c) 2020 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>

"""

from rtloc_manager.manager_api import ManagerPositionApp
import time

class PositionLogger(ManagerPositionApp):
    """  position log app.
    """
    def __init__(self, manager_config, fn):
        super().__init__()

        self.tags = manager_config.tags
        self.log_fn = fn

    def run(self):
        with open(self.log_fn, 'a+') as fh:
            while True:
                position_report = self.pop_report()

                if position_report.device_id in self.tags:
                    dump_str = str(time.time()) + ": " + str(position_report) + "\n"
                    fh.write(dump_str)
