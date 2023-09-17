#! /usr/bin/bash

# Global variables

SCRIPT_DIRECTORY=$(pwd -P)

# Create virtual environment

if [ ! -d "${SCRIPT_DIRECTORY}/pyenv" ]; then
  python3 -m venv pyenv
fi

# Activating virtual environment

# shellcheck source=/dev/null
source "${SCRIPT_DIRECTORY}/pyenv/bin/activate"

# Upgrade Pip

python3 -m pip install --upgrade pip

# Install gRPC 

python3 -m pip install grpcio

# Install gRPC tools (plugin)

python3 -m pip install grpcio-tools

# Compile kvs.proto

python3 -m grpc_tools.protoc -Iprotos --python_out=src --pyi_out=src --grpc_python_out=src protos/kvs.proto

# Leave virtual environment

deactivate