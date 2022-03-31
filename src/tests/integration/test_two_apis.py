import json
import time
from urllib.request import urlopen

import grpc
import pytest
from protobufs.invocation_pb2 import InvocationRequest
from protobufs.invocation_pb2_grpc import InvocationStub
from protobufs.model_pb2 import ModelInput, ModelInputMetadata


@pytest.mark.parametrize('id', [100, 200])
@pytest.mark.parametrize('content', ["0.1,0.2", "0.3,0.4"])
@pytest.mark.parametrize('metadata', [("type", "list"), ("size", "2,1")])
def test_invoke_model(id, content, metadata):
    # submit input
    key, value = metadata
    model_input_metadata_list = [ModelInputMetadata(key=key, value=value)]
    model_input = ModelInput(
        id=id, content=content, metadata=model_input_metadata_list
    )
    request = InvocationRequest(model_input=model_input)
    response = InvocationStub(grpc.insecure_channel("server:8000")).Invoke(request)
    time.sleep(0.1)

    # get invocation info
    response = (
        urlopen(f"http://server:5000/get-invocation-info/{id}").read().decode("utf-8")
    )
    response_dict = json.loads(response)
    assert response_dict["model_input"]["id"] == id
    assert response_dict["model_input"]["content"] == content
    assert response_dict["model_input"]["metadata"][0]["key"] == key
    assert response_dict["model_input"]["metadata"][0]["value"] == value

    assert response_dict["model_output"]["id"] != None
    assert response_dict["model_output"]["metadata"][0]["key"] != None
    assert response_dict["model_output"]["metadata"][0]["value"] != None
