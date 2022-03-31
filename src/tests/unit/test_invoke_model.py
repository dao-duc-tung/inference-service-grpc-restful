import grpc
from protobufs.model_pb2 import ModelInput, ModelInputMetadata
from protobufs.invocation_pb2 import InvocationRequest
from protobufs.invocation_pb2_grpc import InvocationStub


def test_invoke_model():
    model_input_metadata_list = [ModelInputMetadata(key="type", value="list")]
    model_input = ModelInput(
        id=1, content="0.1,0.2", metadata=model_input_metadata_list
    )
    request = InvocationRequest(model_input=model_input)
    response = InvocationStub(grpc.insecure_channel("server:8000")).Invoke(request)
    print(response)
    assert response != None
    assert response.status != ""
