#!/bin/bash

# Organizing proto: https://github.com/protocolbuffers/protobuf/issues/1491#issuecomment-1022571406
python -m grpc_tools.protoc -I . --python_out=src --grpc_python_out=src protobufs/*.proto
