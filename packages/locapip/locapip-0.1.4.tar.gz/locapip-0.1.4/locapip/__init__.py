import importlib
import json
import os
import sys
from pathlib import Path

import grpc
from google.protobuf.json_format import MessageToJson, Parse

sys.path.append(str(os.path.dirname(__file__)))

name = 'locapip'
version = __version__ = '0.1.4'
readme = (Path(os.path.dirname(__file__)) / 'README.md').read_text(encoding='UTF-8')
server = grpc.aio.server()
config = {}


def import_proto(path: str):
    path = str(path)
    sys.path.append(path)

    for p in os.listdir(path):
        if p.endswith('.json') and (Path(path) / p).is_file():
            print(f'config  {Path(path) / p}')
            config.update(json.loads((Path(path) / p).read_text()))

    for p in os.listdir(path):
        if p.endswith('.py') and (Path(path) / p).is_file():
            print(f'import  {Path(path) / p}')
            importlib.import_module(p[:-3])


def import_test():
    import_proto(str(Path(os.path.dirname(__file__)) / '_test'))
    print()


async def serve(port: int) -> None:
    import_test()
    server.add_insecure_port(f'[::]:{port}')
    await server.start()
    await server.wait_for_termination()


pb = {}
stub = {}
py_request = {}
py_response = {}


async def unary_unary(url: str, proto: str, rpc: str, request_type: str, request_json: str, cpp_response_json):
    """
    unary rpc, send single request, receive single response

    :param url: server address
    :param proto: protocol buffer package
    :param rpc: remote procedure call
    :param request_type: request message type
    :param request_json: request json
    :param cpp_response_json: c++ function receive response json
    """
    if proto in py_request and rpc in py_request[proto]:
        py_request_ = py_request[proto][rpc]
    else:
        async def py_request_(request_json_: str):
            request_message_ = Parse(request_json_, getattr(pb[proto], request_type)())
            return request_message_

    if proto in py_response and rpc in py_response[proto]:
        py_response_ = py_response[proto][rpc]
    else:
        async def py_response_(response_message_) -> str:
            response_json_ = MessageToJson(response_message_, True, True)
            return response_json_

    async with grpc.aio.insecure_channel(url) as channel:
        response_message = await getattr(stub[proto](channel), rpc)(await py_request_(request_json))
        response_json = await py_response_(response_message)
        cpp_response_json(response_json)


async def unary_stream(url: str, proto: str, rpc: str, request_type: str, request_json: str, cpp_response_json):
    """
    server streaming rpc, send single request, receive multiple response

    :param url: server address
    :param proto: protocol buffer package name
    :param rpc: remote procedure call name
    :param request_type: request message type name
    :param request_json: request message json string
    :param cpp_response_json: c++ function receive response json
    """
    if proto in py_request and rpc in py_request[proto]:
        py_request_ = py_request[proto][rpc]
    else:
        async def py_request_(request_json_: str):
            request_message_ = Parse(request_json_, getattr(pb[proto], request_type)())
            return request_message_

    if proto in py_response and rpc in py_response[proto]:
        py_response_ = py_response[proto][rpc]
    else:
        async def py_response_(response_message_) -> str:
            response_json_ = MessageToJson(response_message_, True, True)
            return response_json_

    async with grpc.aio.insecure_channel(url) as channel:
        async for response_message in getattr(stub[proto](channel), rpc)(await py_request_(request_json)):
            response_json = await py_response_(response_message)
            cpp_response_json(response_json)


async def stream_unary(url: str, proto: str, rpc: str, request_type: str, cpp_request_json, cpp_response_json):
    """
    client streaming rpc, send multiple request, receive single response

    :param url: server address
    :param proto: protocol buffer package name
    :param rpc: remote procedure call name
    :param request_type: request message type name
    :param cpp_request_json: c++ function send request json
    :param cpp_response_json: c++ function receive response json
    """
    if proto in py_request and rpc in py_request[proto]:
        py_request_ = py_request[proto][rpc]
    else:
        async def py_request_(request_json_: str):
            request_message_ = Parse(request_json_, getattr(pb[proto], request_type)())
            return request_message_

    if proto in py_response and rpc in py_response[proto]:
        py_response_ = py_response[proto][rpc]
    else:
        async def py_response_(response_message_) -> str:
            response_json_ = MessageToJson(response_message_, True, True)
            return response_json_

    async def stream_request():
        while True:
            request_json_ = cpp_request_json()
            if len(request_json_) == 0:
                break
            yield await py_request_(request_json_)

    async with grpc.aio.insecure_channel(url) as channel:
        response_message = await getattr(stub[proto](channel), rpc)(stream_request())
        response_json = await py_response_(response_message)
        cpp_response_json(response_json)


async def stream_stream(url: str, proto: str, rpc: str, request_type: str, cpp_request_json, cpp_response_json):
    """
    bidirectional streaming rpc, send multiple request, receive multiple response

    :param url: server address
    :param proto: protocol buffer package name
    :param rpc: remote procedure call name
    :param request_type: request message type name
    :param cpp_request_json: c++ function send request json
    :param cpp_response_json: c++ function receive response json
    :return: None
    """

    if proto in py_request and rpc in py_request[proto]:
        py_request_ = py_request[proto][rpc]
    else:
        async def py_request_(request_json_: str):
            request_message_ = Parse(request_json_, getattr(pb[proto], request_type)())
            return request_message_

    if proto in py_response and rpc in py_response[proto]:
        py_response_ = py_response[proto][rpc]
    else:
        async def py_response_(response_message_) -> str:
            response_json_ = MessageToJson(response_message_, True, True)
            return response_json_

    async def stream_request():
        while True:
            request_json_ = cpp_request_json()
            if len(request_json_) == 0:
                break
            yield await py_request_(request_json_)

    async with grpc.aio.insecure_channel(url) as channel:
        async for response_message in getattr(stub[proto](channel), rpc)(stream_request()):
            response_json = await py_response_(response_message)
            cpp_response_json(response_json)
