# import asyncio
# from unittest import mock
# import pytest
# from unittest.mock import AsyncMock, MagicMock

# from airzonecloud.AirzoneDevice import *
# from airzonecloud.AirzoneWebsocket import AirzoneWebsocketCLient
# from airzonecloud.AirzoneCloudConnector import AirzoneCloudConnector

# import logging

# logging.basicConfig(level=logging.DEBUG)
# mylogger = logging.getLogger()

# def test_get_device_return_correct_class(mocker):
#     with AsyncMock() as conn_mock:
#         device = AirzoneDevice.get_device({"device_id":1,"type":"az_zone","ws_id":1},conn_mock,None)
#         assert isinstance(device,AirzoneDevice_az_zone)
#         device = AirzoneDevice.get_device({"device_id":1,"type":"az_system","ws_id":1},conn_mock,None)
#         assert isinstance(device,AirzoneDevice_az_system)
#         device = AirzoneDevice.get_device({"device_id":1,"type":"az_ccp","ws_id":1},conn_mock,None)
#         assert isinstance(device,AirzoneDevice_az_ccp)
#         
# def test_get_device_assigns_name_to_new_device_from_data(mocker):
#     with AsyncMock() as conn_mock:
#         device = AirzoneDevice.get_device({"device_id":1,"type":"az_zone","ws_id":1,"name":"new_name"},conn_mock,None)
#         assert device._name == "new_name"

# def test_get_device_assigns_name_to_new_device_if_no_name_in_data(mocker):
#     with AsyncMock() as conn_mock:
#         device = AirzoneDevice.get_device({"device_id":1,"type":"az_zone","ws_id":1},conn_mock,None)
#         assert device._name != ""
#         assert device._name == "Sin nombre az_zone"

# def test_device_appends_listener_to_command_update_on_instantation(mocker): 
#     # prepare a fake connection
#     conn = AirzoneCloudConnector("user","pass")
#     ws_id="ws1"
#     _id="id1"
#     device = AirzoneDevice(_id,ws_id,conn,None)
#     
#     assert  f"DEVICES_UPDATES.{ws_id}.{_id}" in [key for key in  conn.get_websocket()._command_callbacks]

# @pytest.mark.asyncio
# async def test_device_update_listener_is_called_on_right_message(mocker):
#     # prepare a fake connection
#     update_patch = mocker.patch('airzonecloud.AirzoneDevice.AirzoneDevice.update')
#     conn = AirzoneCloudConnector("user","pass")
#     
#     ws_id="ws1"
#     _id="id1"
#     device = AirzoneDevice(_id,ws_id,conn,None)
#     command=[ f"DEVICES_UPDATES.{ws_id}.{_id}" ,{"hello":1}]
#     mylogger.info(command)
#     conn.get_websocket().process_request("42"+json.dumps(command),None)
#     update_patch.assert_awaited_with({"hello":1})
#     

