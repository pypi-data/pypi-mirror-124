import asyncio
import json
import logging
import re
import websockets
from .const import *

logger = logging.getLogger("websockets")
logger.setLevel(logging.INFO)

class AirzoneWebsocketCLient:
    def __init__(self, host="m.airzonecloud.com") -> None:
        self._host = host
        self._ws = None
        self._connected = False
        self._token = None
        self._refresh_token = None
        self._next_command_id = 100
        self._startup_commands = []
        self._events = {}
        self._command_callbacks = {}
        self.add_command_callback("auth", self.authenticate)

    def set_token(self, token, refresh_token):
        self._token = token
        self._refresh_token = refresh_token

    def append_startup_command(self, call, args=None):
        self._startup_commands.append([call, args])

    def add_command_callback(self, command, method):
        if command not in self._command_callbacks:
            self._command_callbacks[command] = []
        self._command_callbacks[command].append(method)

    async def open_client(self):
        if self._token is None:
            raise Exception("Not authenticated")
        if self._connected:
            return
        while True:
            try:
                async with websockets.connect(
                    f"wss://{self._host}/api/v1/websockets/conn/?jwt={self._token}&transport=websocket&EIO=4",
                    origin=f"https://{self._host}",
                    extra_headers={
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "es-419,es;q=0.9,en;q=0.8",
                        "Cache-Control": "no-cache",
                        "Pragma": "no-cache",
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
                    },
                ) as websocket:
                    self._connected = True
                    self._ws = websocket

                    async for message in websocket:
                        await self.process_request(message, websocket)
            except BaseException as e:
                logger.error(e)

    async def process_request(self, message, websocket):

        op_code = re.findall(r"^\D*(\d+)", message[:2])[0]
        if op_code == OP_CODE_CONNECTED:
            await websocket.send(OP_CODE_CONNECTED_ACK)
        if op_code == OP_CODE_CONNECTED_ACK:
            await self.startup(websocket)
        elif op_code == OP_CODE_PING:
            await websocket.send(OP_CODE_PONG)
        elif op_code == OP_CODE_COMMAND:
            command_no = re.findall(r"^(\d*)", message[2:])[0]
            message_data = message[len(OP_CODE_COMMAND) + len(command_no) :]
            await self.response_to_command(command_no, json.loads(message_data))

        elif op_code == OP_CODE_COMMAND_RESPONSE:
            command_no = re.findall(r"^\D*(\d+)", message[2:])[0]
            message_data = message[len(OP_CODE_COMMAND) + len(command_no) :]
            await self.process_response(command_no, json.loads(message_data))

    async def startup(self, ws):
        for f in self._startup_commands:
            if f[1] is None:
                await f[0]()
            else:
                await f[0](*f[1])

    async def response_to_command(self, command_no, message_data):
        if message_data[0] in self._command_callbacks:
            for callback in self._command_callbacks[message_data[0]]:
                await callback(command_no, message_data[1], self)

        else:
            logger.info("commando no registrado:" + message_data[0])

    async def send_command(self, command, data=None):
        self._next_command_id += 1
        req_no = str(self._next_command_id)
        message = OP_CODE_COMMAND + str(req_no)
        if data is not None:
            message += json.dumps([command, data])
        else:
            message += json.dumps([command])
        event = asyncio.Event()
        self._events[req_no] = {"event": event, "data": None}
        await self._ws.send(message)
        a = await self.listen_to_response(req_no)
        return a

    async def clear_listeners(self):
        res = asyncio.create_task(self.send_command("clear_listeners"))

    async def authenticate(self, req_no, data, ws_client):
        if data == "authenticate":
            await self.send_response(req_no, [self._token])

    async def send_response(self, req_no, data):
        await self._ws.send(OP_CODE_COMMAND_RESPONSE + str(req_no) + json.dumps(data))

    async def listen_to_response(self, req_no):
        await self._events[req_no]["event"].wait()
        data = self._events[req_no]["data"]

        return data

    async def process_response(self, req_no, data):
        self._events[req_no]["data"] = data
        self._events[req_no]["event"].set()

    async def listen_instalation(self, installation_id):
        await asyncio.sleep(0.2)
        res = asyncio.create_task(
            self.send_command("listen_installation", installation_id)
        )
        return res
