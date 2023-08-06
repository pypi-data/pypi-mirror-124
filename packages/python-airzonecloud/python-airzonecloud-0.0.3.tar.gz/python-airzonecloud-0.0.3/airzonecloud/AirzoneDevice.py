import asyncio
from abc import abstractmethod
import logging
import json
from .const import *
logger = logging.getLogger("Airzone")
logger.setLevel(logging.INFO) 

class AirzoneDevice:
    def __init__(self, device_id, ws_id, conn, installation, name=None):
        self._conn = conn
        self._installation = installation
        self._id = device_id
        self._name = name
        self._ws_id = ws_id
        self.status = {}
        self.adv_conf = {}
        self.sched_conf = {}
        self.user_conf = {}
        self._callbacks = []
        if getattr(self, "ws_command_listeners", None) is None:
            self.ws_command_listeners = []
        self.ws_command_listeners.append(
            {"command": f"DEVICES_UPDATES.{ws_id}.{self._id}", "method": self.update}
        )
        self.ws_command_listeners.append(
            {"command": "DEVICE_STATE", "method": self.initialize}
        )

        for listener in self.ws_command_listeners:
            conn.get_websocket().add_command_callback(
                listener["command"], listener["method"]
            )

    def add_change_callback(self, callback):
        self._callbacks.append(callback)

    @staticmethod
    def get_device(data, conn, installation):
        _class = globals()["AirzoneDevice_" + data["type"]]
        device = _class(
            data["device_id"],
            data["ws_id"],
            conn,
            installation,
            data.get("name") or ("Sin nombre " + data["type"]),
        )
        return device

    def get_installation(self):
        return self._installation

    async def update(self, command_no, message_data, ws_client):
        try:
            for setting in message_data["change"]:
                for key, value in message_data["change"][setting].items():
                    self.__getattribute__(setting)[key] = value

        except:
            logger.exception(json.dumps(message_data))
        for callback in self._callbacks:
            callback()

    async def initialize(self, command_no, message_data, ws_client):
        if message_data["device_id"] == self._id:

            self.status = message_data["status"]
            self.adv_conf = message_data.get("adv_conf", {})

    @abstractmethod
    async def get_capabilities(self):
        pass


class AirzoneDevice_az_ccp(AirzoneDevice):
    pass


class AirzoneDevice_az_system(AirzoneDevice):
    def __init__(self, device_id, ws_id, conn, installation, name=None):
        self.ws_command_listeners=[]
        super().__init__(device_id, ws_id, conn, installation, name)

    async def get_capabilities(self):
        while self.status == {}:
            await asyncio.sleep(0.1)
        return self.status

    async def set_mode(self, mode):
        await self._conn.patch(
            f"/devices/{self._id}",
            {
                "installation_id": self._installation._id,
                "opts": {"units": CONST_CELSIUS},
                "param": "mode",
                "value": mode,
            },
        )

    async def set_power(self, power):
        self.status["power"] = power
        await self._conn.patch(
            f"/devices/{self._id}",
            {
                "installation_id": self._installation._id,
                "opts": {"units": CONST_CELSIUS},
                "param": "power",
                "value": power,
            },
        )


class AirzoneDevice_az_zone(AirzoneDevice):
    async def get_capabilities(self):
        while self.status == {}:
            await asyncio.sleep(0.1)
        return self.status

    async def set_temperature(self, temperature: float):
        await self._conn.patch(
            f"/devices/{self._id}",
            {
                "installation_id": self._installation._id,
                "opts": {"units": CONST_CELSIUS},
                "param": "setpoint_air_heat",
                "value": temperature,
            },
        )

    async def set_mode(self, mode):
        await self._conn.patch(
            f"/devices/{self._id}",
            {
                "installation_id": self._installation._id,
                "opts": {"units": CONST_CELSIUS},
                "param": "mode",
                "value": mode,
            },
        )

    async def set_power(self, power):
        self.status["power"] = power
        await self._conn.patch(
            f"/devices/{self._id}",
            {
                "installation_id": self._installation._id,
                "opts": {"units": CONST_CELSIUS},
                "param": "power",
                "value": power,
            },
        )
