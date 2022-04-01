import os

import grpc
import pytest
from protobufs.invocation_pb2 import InvocationRequest
from protobufs.invocation_pb2_grpc import InvocationStub
from protobufs.model_pb2 import ModelInput, ModelInputMetadata
from utils import DefaultApiValues

SERVER_HOST_NAME = os.getenv("SERVER_HOST_NAME", DefaultApiValues.SERVER_HOST_NAME)
GRPC_PORT = os.getenv("GRPC_PORT", DefaultApiValues.GRPC_PORT)


@pytest.mark.slow
@pytest.mark.parametrize("id", [1])
@pytest.mark.parametrize("content", ["0.1,0.2"])
@pytest.mark.parametrize("metadata", [("type", "list")])
def test_invoke_model(id, content, metadata):
    key, value = metadata
    model_input_metadata_list = [ModelInputMetadata(key=key, value=value)]
    model_input = ModelInput(id=id, content=content, metadata=model_input_metadata_list)
    request = InvocationRequest(model_input=model_input)
    channel = grpc.insecure_channel(f"{SERVER_HOST_NAME}:{GRPC_PORT}")
    client = InvocationStub(channel)
    response = client.Invoke(request)
    assert response != None
    assert response.status != ""
