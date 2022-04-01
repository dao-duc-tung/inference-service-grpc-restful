import os
from urllib.request import urlopen

import pytest

SERVER_HOST_NAME = os.getenv("SERVER_HOST_NAME", "server")
REST_PORT = os.getenv("REST_PORT", "server")


@pytest.mark.parametrize("execution_number", range(1))
def test_ping(execution_number):
    # don't work with http://0.0.0.0:port, http://127.0.0.1:port
    # or server:port, MUST BE http://server:port
    ping_page = (
        urlopen(f"http://{SERVER_HOST_NAME}:{REST_PORT}/").read().decode("utf-8")
    )
    assert "ready" in ping_page
