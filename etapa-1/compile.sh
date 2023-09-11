#! /usr/bin/bash

# falta comandos para instalar requisitos

# compila kvs.proto
var=`python3 -m grpc_tools.protoc -Iprotos --python_out=src --pyi_out=src --grpc_python_out=src protos/kvs.proto`
echo $var

