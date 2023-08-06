import asyncio
import importlib
import os
import sys
from pathlib import Path

import grpc
from google.protobuf.json_format import Parse, MessageToJson

sys.path.append(str(os.path.dirname(__file__)))

name = 'locapip'
version = __version__ = '0.1.7'
server = grpc.aio.server()
config = {}


def import_package(path: str):
    path = str(path)
    sys.path.append(path)

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
py_request = {}
py_response = {}


def _py_request_unary(request_type):
    async def foo(cpp_request_):
        return Parse(cpp_request_(str()), request_type())

    return foo


def _py_request_stream(request_type):
    async def foo(cpp_request_):
        while True:
            request_json_ = cpp_request_(str())
            if len(request_json_) == 0:
                break
            yield Parse(request_json_, request_type())

    return foo


async def _py_response_unary(response_message, cpp_response, *args):
    response_json = MessageToJson(response_message, True, True)
    cpp_response(response_json)


async def _py_response_stream(response_message_iterator, cpp_response, *args):
    async for response_message_ in response_message_iterator:
        cpp_response(MessageToJson(response_message_, True, True))
    cpp_response(str())


async def _run(url: str, package: str, rpc: str, py_request_argv, py_response_argv):
    async with grpc.aio.insecure_channel(url) as channel:
        stub_ = getattr(stub[package](channel), rpc)
        if 'UnaryUnary' in str(stub_.__class__):
            py_request_default = _py_request_unary
            py_response_default = _py_response_unary
        elif 'UnaryStream' in str(stub_.__class__):
            py_request_default = _py_request_unary
            py_response_default = _py_response_stream
        elif 'StreamUnary' in str(stub_.__class__):
            py_request_default = _py_request_stream
            py_response_default = _py_response_unary
        elif 'StreamStream' in str(stub_.__class__):
            py_request_default = _py_request_stream
            py_response_default = _py_response_stream

        if package in py_request and rpc in py_request[package]:
            if importlib.import_module(py_request[package][rpc].__module__) is pb[package]:
                py_request_ = py_request_default(py_request[package][rpc])
            else:
                py_request_ = py_request[package][rpc]
        else:
            raise NotImplementedError(f'{package} {rpc} py_request not implemented')

        if package in py_response and rpc in py_response[package]:
            py_response_ = py_response[package][rpc]
        else:
            py_response_ = py_response_default

        if 'UnaryUnary' in str(stub_.__class__):
            response_message = await stub_(await py_request_(*py_request_argv))

        elif 'UnaryStream' in str(stub_.__class__):
            response_message = stub_(await py_request_(*py_request_argv))
        elif 'StreamUnary' in str(stub_.__class__):
            response_message = await stub_(py_request_(*py_request_argv))
        elif 'StreamStream' in str(stub_.__class__):
            response_message = stub_(py_request_(*py_request_argv))
        await py_response_(response_message, *py_response_argv)


def run(url: str, package: str, rpc: str, request, response):
    """
    async run rpc in package on server at url, see specification in each package.py

    :param url: server address
    :param package: protocol buffer package
    :param rpc: remote procedure call
    :param request: vector<function<string<string>>> in py_request
    :param response: vector<function<string<string>>> in py_response
    """

    asyncio.get_event_loop().run_until_complete(_run(url, package, rpc, request, response))
