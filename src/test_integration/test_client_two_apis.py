import json
import os
import time
from urllib.error import HTTPError
from urllib.request import urlopen

import grpc
import pytest
from model_module.utils import ImgUtils
from protobufs.invocation_pb2 import InvocationRequest
from protobufs.invocation_pb2_grpc import InvocationStub
from protobufs.model_pb2 import ModelInput, ModelInputMetadata
from utils import DefaultApiValues, RestApiDefinition

SERVER_HOST_NAME = "localhost"
GRPC_PORT = os.getenv("GRPC_PORT", DefaultApiValues.GRPC_PORT)
REST_PORT = os.getenv("REST_PORT", DefaultApiValues.REST_PORT)
WAIT_TIME = 0.2


@pytest.mark.client
@pytest.mark.slow
@pytest.mark.parametrize("id", [100])
@pytest.mark.parametrize("content", ["0.1,0.2"])
@pytest.mark.parametrize("metadata", [("type", "list")])
def test_two_apis_bad_content(id, content, metadata):
    key, value = metadata
    model_input_metadata_list = [ModelInputMetadata(key=key, value=value)]
    model_input = ModelInput(id=id, content=content, metadata=model_input_metadata_list)
    request = InvocationRequest(model_input=model_input)
    channel = grpc.insecure_channel(f"{SERVER_HOST_NAME}:{GRPC_PORT}")
    client = InvocationStub(channel)
    response = client.Invoke(request)
    time.sleep(WAIT_TIME)

    try:
        urlopen(
            f"http://{SERVER_HOST_NAME}:{REST_PORT}/{RestApiDefinition.GET_INVOCATION_INFO}/{id}"
        )
    except HTTPError as ex:
        assert ex.code == 404


@pytest.mark.client
@pytest.mark.slow
@pytest.mark.parametrize("id", [111])
@pytest.mark.parametrize("img_path", ["../images/lenna.png"])
@pytest.mark.parametrize("metadata", [[]])
def test_two_apis_good_content(id, img_path, metadata):
    base64_str = ImgUtils.img_path_to_base64_str(img_path)
    model_input = ModelInput(id=id, content=base64_str, metadata=metadata)
    request = InvocationRequest(model_input=model_input)
    channel = grpc.insecure_channel(f"{SERVER_HOST_NAME}:{GRPC_PORT}")
    client = InvocationStub(channel)
    response = client.Invoke(request)
    time.sleep(WAIT_TIME)

    response = (
        urlopen(
            f"http://{SERVER_HOST_NAME}:{REST_PORT}/{RestApiDefinition.GET_INVOCATION_INFO}/{id}"
        )
        .read()
        .decode("utf-8")
    )
    response_dict = json.loads(response)

    assert "model_input" in response_dict
    assert "model_output" in response_dict

    assert response_dict["model_input"]["id"] == id
    assert response_dict["model_input"]["content"] == base64_str.decode("utf-8")
    assert len(response_dict["model_input"]["metadata"]) == 0

    assert response_dict["model_output"]["id"] == id
    assert len(response_dict["model_output"]["metadata"]) == 1
