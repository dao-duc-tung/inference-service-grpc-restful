import os
from urllib.request import urlopen

import pytest

SERVER_HOST_NAME = os.getenv("SERVER_HOST_NAME", "server")


@pytest.mark.parametrize("id", [1, 2])
def test_get_invocation_info(id):
    response = (
        urlopen(f"http://{SERVER_HOST_NAME}:5000/get-invocation-info/{id}")
        .read()
        .decode("utf-8")
    )
    assert "model_input" in response or "message" in response
