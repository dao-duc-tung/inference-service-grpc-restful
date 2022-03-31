from urllib.request import urlopen

import pytest


@pytest.mark.parametrize('execution_number', range(2))
def test_ping(execution_number):
    # don't work with http://0.0.0.0:5000, http://127.0.0.1:5000
    # or server:5000, MUST BE http://server:5000
    ping_page = urlopen("http://server:5000").read().decode("utf-8")
    assert "Welcome" in ping_page
