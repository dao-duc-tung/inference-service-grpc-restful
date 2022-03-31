from urllib.request import urlopen


def test_ping():
    ping_page = urlopen("http://server:5000").read().decode("utf-8")
    assert "Welcome" in ping_page
