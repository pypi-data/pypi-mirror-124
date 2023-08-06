from .AirzoneCloudConnector import AirzoneCloudConnector
from .AirzoneDevice import AirzoneDevice, AirzoneDevice_az_system
import asyncio


class AirzoneInstallation:
    def __init__(self, installation_id, conn=None, email=None, password=None):
        if conn is None:
            conn = AirzoneCloudConnector(email, password)
        self._conn = conn
        self._id = installation_id
        self._inited = False
        self.devices = []
        self.system_device = None

    async def start(self):
        data = await self._conn.get_installation(self._id)
        if data:
            self._inited = True
            for group in data["groups"]:
                for device in group["devices"]:
                    dev = AirzoneDevice.get_device(device, self._conn, self)
                    self.devices.append(dev)
                    if isinstance(dev, AirzoneDevice_az_system):
                        self.system_device = dev

    async def connect_live_updates(self):
        ws_client = self._conn.get_websocket()
        ws_client.append_startup_command(ws_client.listen_instalation, (self._id,))
        asyncio.create_task(self._conn.get_websocket().open_client())
