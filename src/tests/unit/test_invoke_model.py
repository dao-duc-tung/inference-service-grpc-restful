import grpc
import pytest
from protobufs.invocation_pb2 import InvocationRequest
from protobufs.invocation_pb2_grpc import InvocationStub
from protobufs.model_pb2 import ModelInput, ModelInputMetadata


@pytest.mark.parametrize('id', [1, 2])
@pytest.mark.parametrize('content', ["0.1,0.2", "0.3,0.4"])
@pytest.mark.parametrize('metadata', [("type", "list"), ("size", "2,1")])
def test_invoke_model(id, content, metadata):
    key, value = metadata
    model_input_metadata_list = [ModelInputMetadata(key=key, value=value)]
    model_input = ModelInput(
        id=id, content=content, metadata=model_input_metadata_list
    )
    request = InvocationRequest(model_input=model_input)
    response = InvocationStub(grpc.insecure_channel("server:8000")).Invoke(request)
    assert response != None
    assert response.status != ""
