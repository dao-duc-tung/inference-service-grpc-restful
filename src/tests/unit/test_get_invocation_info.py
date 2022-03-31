from urllib.request import urlopen

import pytest


@pytest.mark.parametrize('id', [1, 2])
def test_get_invocation_info(id):
    response = (
        urlopen(f"http://server:5000/get-invocation-info/{id}").read().decode("utf-8")
    )
    assert "model_input" in response or "message" in response
