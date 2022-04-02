import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: Tests that run in > ~1 seconds.")
    config.addinivalue_line("markers", "client: Tests that run outside the containers.")


def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )
    parser.addoption(
        "--client", action="store_true", default=False, help="run client tests"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        return

    skip_slow = pytest.mark.skip(reason="it takes time")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
