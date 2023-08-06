import asyncio

from google.protobuf.json_format import Parse, MessageToJson

import locapip
import locapip_test_pb2 as pb
import locapip_test_pb2_grpc as pb_rpc


class Service(pb_rpc.TestServicer):
    async def unary_unary(self, request, context):
        print('---------- Test unary_unary ----------')
        print('server receive')
        print(MessageToJson(request, True, True))
        response = pb.Text(text=f'py_response')
        print('server send')
        print(MessageToJson(response, True, True))
        return response

    async def unary_stream(self, request, context):
        print('---------- Test unary_stream ----------')
        print('server receive')
        print(MessageToJson(request, True, True))
        for _ in range(3):
            response = pb.Text(text=f'py_response {_ + 1}')
            print('server send')
            print(MessageToJson(response, True, True))
            yield response

    async def stream_unary(self, request_iterator, context):
        print('---------- Test stream_unary ----------')
        t = []
        async for request in request_iterator:
            print('server receive')
            print(MessageToJson(request, True, True))
            t.append(request.text)
        response = pb.Text(text=f'py_response {len(t)}')
        print('server send')
        print(MessageToJson(response, True, True))
        return response

    async def stream_stream(self, request_iterator, context):
        print('---------- Test stream_unary ----------')
        t = []
        async for request in request_iterator:
            print('server receive')
            print(MessageToJson(request, True, True))
            t.append(request.text)
            response = pb.Text(text=f'py_response {len(t)}')
            print('server send')
            print(MessageToJson(response, True, True))
            yield response


async def py_request(request_json: str):
    request_message = Parse(request_json, pb.Text())
    print(f'client {py_request.__name__}')
    print(MessageToJson(request_message, True, True))
    return request_message


async def py_request_delay(request_json: str):
    await asyncio.sleep(1)
    return await py_request(request_json)


async def py_response(response_message) -> str:
    response_json = MessageToJson(response_message, True, True)
    print(f'client {py_response.__name__}')
    print(response_json)
    return response_json


pb_rpc.add_TestServicer_to_server(Service(), locapip.server)
locapip.pb['locapip_test'] = pb
locapip.stub['locapip_test'] = pb_rpc.TestStub

locapip.py_request['locapip_test'] = {'unary_unary': py_request,
                                      'unary_stream': py_request,
                                      'stream_unary': py_request,
                                      'stream_stream': py_request_delay}
locapip.py_response['locapip_test'] = {'unary_unary': py_response,
                                       'unary_stream': py_response,
                                       'stream_unary': py_response,
                                       'stream_stream': py_response}
