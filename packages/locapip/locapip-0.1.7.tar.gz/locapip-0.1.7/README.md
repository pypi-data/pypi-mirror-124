# C++嵌入式Python微服务

C++ embedded Python microservices

## 1 简介

locapip是一个小型gRPC运行框架，适用于内置Python解释器的C++项目。

结合locapic，可与虚幻引擎项目优雅集成

## 2 服务端

### 2.1 启动

安装

```
python -m pip install locapip
```

启动服务

```
python -m locapip --port 6547 --proto PROTOBUF_DIR
```

其中，```PROTOBUF_DIR```是你的protobuf目录，应包含

```
PROTOBUF_DIR
    ├ example.py            服务端的实现，通常也包含客户端的实现
    ├ example_pb2.py        protobuf生成文件
    ├ example_pb2_grpc.py   grpc生成文件
```

### 2.2 实现

服务端在```example.py```中实现，请参阅 [gRPC Python](https://grpc.io/docs/languages/python/)
和 [Examples](https://github.com/grpc/grpc/tree/master/examples)

## 3 客户端

### 3.1 Python

服务端和客户端都应能够访问同一版本的protobuf目录，在运行时```import```该目录下的所有模块，因此客户端也在```example.py```中实现。

### 3.2 C++

需结合C++接口locapic使用

locapic，借助pybind11的嵌入式Python解释器，提供了一套通用的C++接口使用locapip

TODO