import json
import os
import time
from urllib.request import urlopen

import grpc
from model_module.utils import ImgUtils
from protobufs.invocation_pb2 import InvocationRequest
from protobufs.invocation_pb2_grpc import InvocationStub
from protobufs.model_pb2 import ModelInput, ModelInputMetadata
from utils import DefaultApiValues, RestApiDefinition

SERVER_HOST_NAME = "localhost"
GRPC_PORT = os.getenv("GRPC_PORT", DefaultApiValues.GRPC_PORT)
REST_PORT = os.getenv("REST_PORT", DefaultApiValues.REST_PORT)
WAIT_TIME = 0.2
ID = 1
IMG_PATH = "../images/lenna.png"


def invoke_model(id, img_base64):
    model_input_metadata = [ModelInputMetadata(key="type", value="image")]
    model_input = ModelInput(id=id, content=img_base64, metadata=model_input_metadata)

    request = InvocationRequest(model_input=model_input)
    channel = grpc.insecure_channel(f"{SERVER_HOST_NAME}:{GRPC_PORT}")
    client = InvocationStub(channel)
    response = client.Invoke(request)


def get_invocation_info(id):
    response = urlopen(
        f"http://{SERVER_HOST_NAME}:{REST_PORT}/{RestApiDefinition.INVOCATION}/{id}"
    )
    response = response.read().decode("utf-8")
    response_dict = json.loads(response)
    return response_dict


def assert_response(response_dict, id, img_base64):
    assert "model_input" in response_dict
    assert "model_output" in response_dict

    assert response_dict["model_input"]["id"] == id
    assert response_dict["model_input"]["content"] == img_base64.decode("utf-8")
    assert len(response_dict["model_input"]["metadata"]) == 1

    assert response_dict["model_output"]["id"] == id
    assert len(response_dict["model_output"]["metadata"]) == 1

    # remove image content to print out result
    response_dict["model_input"].pop("content")
    print(response_dict)


def quick_start(id, img_path):
    img_base64 = ImgUtils.img_path_to_base64_str(img_path)

    invoke_model(id, img_base64)
    time.sleep(WAIT_TIME)
    response_dict = get_invocation_info(id)

    assert_response(response_dict, id, img_base64)


if __name__ == "__main__":
    quick_start(ID, IMG_PATH)
