import os
from urllib.request import urlopen

import pytest

SERVER_HOST_NAME = os.getenv("SERVER_HOST_NAME", "server")
REST_PORT = os.getenv("REST_PORT", "5000")


@pytest.mark.parametrize("id", [1])
def test_get_invocation_info(id):
    response = (
        urlopen(f"http://{SERVER_HOST_NAME}:{REST_PORT}/get-invocation-info/{id}")
        .read()
        .decode("utf-8")
    )
    assert "model_input" in response or "message" in response
