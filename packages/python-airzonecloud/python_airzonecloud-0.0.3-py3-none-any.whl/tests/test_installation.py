import asyncio
import pytest
from airzonecloud.AirzoneDevice import AirzoneDevice_az_system

from airzonecloud.AirzoneInstallation import AirzoneInstallation, AirzoneCloudConnector
from unittest.mock import AsyncMock, MagicMock

def test_if_provided_connection_uses_that_connection():
    conn = object()
    installation = AirzoneInstallation("1",conn=conn, email="j@j.com",password="1234")
    assert conn == installation._conn
    
def test_if_not_connexion_create_one():
    installation = AirzoneInstallation("1",email="j@j.com",password="1234")
    assert isinstance(installation._conn,AirzoneCloudConnector)

@pytest.mark.asyncio
async def test_installation_start_get_installation_info(mocker):
    get_installation_patch = mocker.patch('airzonecloud.AirzoneCloudConnector.AirzoneCloudConnector.get_installation', return_value=[])
    installation = AirzoneInstallation("1",email="j@j.com",password="1234")
    a = await installation.start()
    assert await get_installation_patch.called_once()


@pytest.mark.asyncio
async def test_installation_start_create_installation_devices(mocker):
    get_installation_patch = mocker.patch('airzonecloud.AirzoneCloudConnector.AirzoneCloudConnector.get_installation', return_value={"groups":[{"devices":[{"id":1},{"id":2}]}]})
    get_device_patch = mocker.patch('airzonecloud.AirzoneDevice.AirzoneDevice.get_device', return_value=[])
    installation = AirzoneInstallation("1",email="j@j.com",password="1234")
    a = await installation.start()
    assert get_device_patch.call_count ==2

@pytest.mark.asyncio
async def test_installation_start_if_device_is_system_the_installation_saves_it_as_master(mocker):
    get_installation_patch = mocker.patch('airzonecloud.AirzoneCloudConnector.AirzoneCloudConnector.get_installation', return_value={"groups":[{"devices":[{"device_id":1,"type":"az_system","ws_id":"1"}]}]})
    installation = AirzoneInstallation("1",email="j@j.com",password="1234")
    a = await installation.start()
    assert installation.system_device is not None
    assert isinstance(installation.system_device , AirzoneDevice_az_system)

@pytest.mark.asyncio
async def test_installation_append_installation_listener_to_the_connection(mocker):
    my_mock= AsyncMock()
    get_websocket_patch = my_mock.patch('airzonecloud.AirzoneCloudConnector.AirzoneCloudConnector.get_websocket')
    installation = AirzoneInstallation("1",email="j@j.com",password="1234")
    await installation.connect_live_updates()
    assert my_mock.called_once()

        
