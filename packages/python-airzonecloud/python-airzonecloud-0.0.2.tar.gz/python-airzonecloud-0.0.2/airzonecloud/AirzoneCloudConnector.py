import aiohttp
import asyncio
from .AirzoneWebsocket import AirzoneWebsocketCLient



class AirzoneCloudConnector:
    def __init__(
        self,
        user,
        password,
        host="m.airzonecloud.com",
        protocol="https",
        api_path="/api/v1",
    ):
        self._user = user
        self._password = password
        self._host = host
        self._protocol = protocol
        self._api_path = api_path
        self._connected = False
        self._token = None
        self._refresh_token = None
        self._base_url = f"{self._protocol}://{self._host}{self._api_path}"
        self.ws_client = AirzoneWebsocketCLient()

        self.ws_client.append_startup_command(self.ws_client.clear_listeners)
        self.ws_client.append_startup_command(self.ws_client.clear_listeners)

    def get_websocket(self):
        return self.ws_client

    async def get(self, method, query_params={}, headers={}, authenticate=True):
        if authenticate:
            if not self._connected:
                raise Exception("Not connected")
            headers["authorization"] = f"Bearer {self._token}"
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self._base_url + method, headers=headers
            ) as response:
                if "application/json" in response.headers.get("content-type", ""):
                    return await response.json()
                return await response.text()

    async def post(self, method, body={}, headers={}, authenticate=True):
        if authenticate:
            if not self._connected:
                raise Exception("Not connected")
            headers["authorization"] = f"Bearer {self._token}"
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self._base_url + method, json=body, headers=headers
            ) as response:
                if "application/json" in response.headers.get("content-type", ""):
                    return await response.json()
                return await response.text()

    async def patch(self, method, body=None, headers=None, authenticate=True):
        if headers is None:
            headers = {}

        if authenticate:
            if not self._connected:
                raise Exception("Not connected")
            headers["authorization"] = f"Bearer {self._token}"
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                self._base_url + method, json=body, headers=headers
            ) as response:
                if "application/json" in response.headers.get("content-type", ""):
                    return await response.json()
                return await response.text()

    async def connect(self):
        if self._connected:
            return True
        response = await self.post(
            "/auth/login",
            {"email": self._user, "password": self._password},
            authenticate=False,
        )
        self._token = response["token"]
        self._refresh_token = response["refreshToken"]
        self._connected = True
        self.ws_client.set_token(self._token, self._refresh_token)
        return True

    async def refresh_connection(self):
        response = await self.get(f"/auth/refreshToken/{self._refresh_token}")
        self._token = response["token"]
        self._refresh_token = response["refreshToken"]
        self._connected = True
        return True

    async def get_installations(self):
        if not self._connected:
            await self.connect()
        response = await self.get("/installations")
        return response["installations"]

    async def get_installation(self, installation_id):
        if not self._connected:
            await self.connect()
        return await self.get(f"/installations/{installation_id}")

    async def get_location(self, location_id):
        if not self._connected:
            await self.connect()
        return await self.get(f"/installations/location/{location_id}")
