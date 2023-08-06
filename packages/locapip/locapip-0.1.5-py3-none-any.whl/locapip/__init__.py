import asyncio
import importlib
import json
import os
import sys
from pathlib import Path

import grpc
from google.protobuf.json_format import Parse, MessageToJson

sys.path.append(str(os.path.dirname(__file__)))

name = 'locapip'
version = __version__ = '0.1.5'
readme = (Path(os.path.dirname(__file__)) / 'README.md').read_text(encoding='UTF-8')
server = grpc.aio.server()
config = {}


def import_package(path: str):
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


def import_package_test():
    import_package(str(Path(os.path.dirname(__file__)) / '_test'))
    print()


async def serve(port: int) -> None:
    import_package_test()
    server.add_insecure_port(f'[::]:{port}')
    await server.start()
    await server.wait_for_termination()


pb = {}
stub = {}
service = {}
py_request = {}
py_response = {}


def run(url: str, package: str, rpc: str, request, response):
    """

    :param url: server address
    :param package: protocol buffer package
    :param rpc: remote procedure call
    :param request: vector<function<string<string>>> in py_request
    :param response: vector<function<string<string>>> in py_response
    """

    if package in service and rpc in service[package]:
        asyncio.get_event_loop().run_until_complete(service[package][rpc](url, package, rpc, request, response))
    else:
        raise NotImplementedError(f'{package} {rpc} service not implemented')


async def unary_unary(url: str, package: str, rpc: str, py_request_argv, py_response_argv):
    if package in py_request and rpc in py_request[package]:
        if importlib.import_module(py_request[package][rpc].__module__) is pb[package]:
            async def py_request_(cpp_request_):
                return Parse(cpp_request_(''), py_request[package][rpc]())
        else:
            py_request_ = py_request[package][rpc]
    else:
        raise NotImplementedError(f'{package} {rpc} py_request not implemented')

    if package in py_response and rpc in py_response[package]:
        if importlib.import_module(py_response[package][rpc].__module__) is pb[package]:
            async def py_response_(response_message_, cpp_response_json):
                response_json = MessageToJson(response_message_, True, True)
                response_message_ = Parse(response_json, py_response[package][rpc](), True)
                response_json = MessageToJson(response_message_, True, True)
                cpp_response_json(response_json)
        else:
            py_response_ = py_response[package][rpc]
    else:
        async def py_response_(response_message_, cpp_response_json):
            response_json = MessageToJson(response_message_, True, True)
            cpp_response_json(response_json)

    async with grpc.aio.insecure_channel(url) as channel:
        stub_ = stub[package](channel)
        response_message = await getattr(stub_, rpc)(await py_request_(*py_request_argv))
        await py_response_(response_message, *py_response_argv)


async def unary_stream(url: str, package: str, rpc: str, py_request_argv, py_response_argv):
    if package in py_request and rpc in py_request[package]:
        if importlib.import_module(py_request[package][rpc].__module__) is pb[package]:
            async def py_request_(cpp_request_):
                return Parse(cpp_request_(''), py_request[package][rpc]())
        else:
            py_request_ = py_request[package][rpc]
    else:
        raise NotImplementedError(f'{package} {rpc} py_request not implemented')

    if package in py_response and rpc in py_response[package]:
        if importlib.import_module(py_response[package][rpc].__module__) is pb[package]:
            async def py_response_(response_message_, cpp_response_json):
                response_json = MessageToJson(response_message_, True, True)
                response_message_ = Parse(response_json, py_response[package][rpc](), True)
                response_json = MessageToJson(response_message_, True, True)
                cpp_response_json(response_json)
        else:
            py_response_ = py_response[package][rpc]
    else:
        async def py_response_(response_message_, cpp_response_json):
            response_json = MessageToJson(response_message_, True, True)
            cpp_response_json(response_json)

    async with grpc.aio.insecure_channel(url) as channel:
        stub_ = stub[package](channel)
        response_message_iterator = getattr(stub_, rpc)(await py_request_(*py_request_argv))
        async for response_message in response_message_iterator:
            await py_response_(response_message, *py_response_argv)


async def stream_unary(url: str, package: str, rpc: str, py_request_argv, py_response_argv):
    if package in py_request and rpc in py_request[package]:
        if importlib.import_module(py_request[package][rpc].__module__) is pb[package]:
            async def py_request_(cpp_request_):
                while True:
                    request_json_ = cpp_request_('')
                    if len(request_json_) == 0:
                        break
                    yield Parse(request_json_, py_request[package][rpc]())
        else:
            py_request_ = py_request[package][rpc]
    else:
        raise NotImplementedError(f'{package} {rpc} py_request not implemented')

    if package in py_response and rpc in py_response[package]:
        if importlib.import_module(py_response[package][rpc].__module__) is pb[package]:
            async def py_response_(response_message_, cpp_response_json):
                response_json = MessageToJson(response_message_, True, True)
                response_message_ = Parse(response_json, py_response[package][rpc](), True)
                response_json = MessageToJson(response_message_, True, True)
                cpp_response_json(response_json)
        else:
            py_response_ = py_response[package][rpc]
    else:
        async def py_response_(response_message_, cpp_response_json):
            response_json = MessageToJson(response_message_, True, True)
            cpp_response_json(response_json)

    async with grpc.aio.insecure_channel(url) as channel:
        stub_ = stub[package](channel)
        response_message = await getattr(stub_, rpc)(py_request_(*py_request_argv))
        await py_response_(response_message, *py_response_argv)


async def stream_stream(url: str, package: str, rpc: str, py_request_argv, py_response_argv):
    if package in py_request and rpc in py_request[package]:
        if importlib.import_module(py_request[package][rpc].__module__) is pb[package]:
            async def py_request_(cpp_request_):
                while True:
                    await asyncio.sleep(1)
                    request_json_ = cpp_request_('')
                    if len(request_json_) == 0:
                        break
                    yield Parse(request_json_, py_request[package][rpc]())
        else:
            py_request_ = py_request[package][rpc]
    else:
        raise NotImplementedError(f'{package} {rpc} py_request not implemented')

    if package in py_response and rpc in py_response[package]:
        if importlib.import_module(py_response[package][rpc].__module__) is pb[package]:
            async def py_response_(response_message_, cpp_response_json):
                response_json = MessageToJson(response_message_, True, True)
                response_message_ = Parse(response_json, py_response[package][rpc](), True)
                response_json = MessageToJson(response_message_, True, True)
                cpp_response_json(response_json)
        else:
            py_response_ = py_response[package][rpc]
    else:
        async def py_response_(response_message_, cpp_response_json):
            response_json = MessageToJson(response_message_, True, True)
            cpp_response_json(response_json)

    async with grpc.aio.insecure_channel(url) as channel:
        stub_ = stub[package](channel)
        response_message_iterator = getattr(stub_, rpc)(py_request_(*py_request_argv))
        async for response_message in response_message_iterator:
            await py_response_(response_message, *py_response_argv)
