from urllib.request import urlopen


def test_get_invocation_info():
    response = (
        urlopen("http://server:5000/get-invocation-info/1").read().decode("utf-8")
    )
    assert "model_input" in response or "message" in response
