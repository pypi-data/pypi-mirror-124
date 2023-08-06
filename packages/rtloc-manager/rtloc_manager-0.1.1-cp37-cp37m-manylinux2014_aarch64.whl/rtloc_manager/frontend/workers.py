import asyncio

from PySide2.QtCore import QRunnable

class AlarmToggleWorker(QRunnable):
    def __init__(self, silence_group_id):
        """ Create and Alarm Toggle Worker object

        Args:
            silence_group (int): silence group id between 1-15. group id 0 is reserved
            for roaming tags to not breach each other.
        """
        super().__init__()

        self.selected_ble_device = None
        self.silence_group_id = int(silence_group_id)

        # enforce group id range
        if self.silence_group_id < 1 or self.silence_group_id > 15:
            raise ValueError("Given group id should be an integer from 1 to 15 (inclusive)")

    def run(self):
        print("[START] alarm toggle worker")
        if self.selected_ble_device is not None:
            fut = asyncio.run_coroutine_threadsafe(self._run(), self.event_loop)
            fut.result()
        print("[STOP] alarm toggle worker")

    def set_device_name(self, device_name):
        self.selected_ble_device = device_name

    def set_event_loop(self, event_loop):
        self.event_loop = event_loop

    async def _run(self):
        try:
            await self._connect()
        except DeviceNotFoundError:
            print("Device not found error. Is the device advertising?")
            return

        await self._toggle()
        await self._disconnect()

    async def _connect(self):
        import bleak
        import rtloc_ble.api as ble_api

        print("selected device:", self.selected_ble_device)
        self.dev = await ble_api.get_ble_client_for_device(self.selected_ble_device)

        if self.dev is None:
            raise DeviceNotFoundError

        self.client = bleak.BleakClient(self.dev)
        await self.client.connect()

    async def _toggle(self):
        import rtloc_ble.api as ble_api

        lsb, msb = await ble_api.get_group_ids(self.client)

        group_id = (msb << 8) + lsb
        group_id = group_id ^ (1 << self.silence_group_id)

        lsb = group_id & 15
        msb = group_id >> 8

        await ble_api.set_group_ids(self.client, silence_group=lsb, friend_group=msb)

    async def _disconnect(self):
        await self.client.disconnect()


class DeviceNotFoundError(Exception):
    pass
