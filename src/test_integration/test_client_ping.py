import os
from urllib.request import urlopen

import pytest
from utils import DefaultApiValues, RestApiDefinition

SERVER_HOST_NAME = "localhost"
REST_PORT = os.getenv("REST_PORT", DefaultApiValues.REST_PORT)


@pytest.mark.client
@pytest.mark.parametrize("execution_number", range(1))
def test_client_ping(execution_number):
    # don't work with http://0.0.0.0:port, http://127.0.0.1:port
    # or server:port, MUST BE http://server:port
    ping_page = (
        urlopen(f"http://{SERVER_HOST_NAME}:{REST_PORT}/{RestApiDefinition.PING}")
        .read()
        .decode("utf-8")
    )
    assert "ready" in ping_page
