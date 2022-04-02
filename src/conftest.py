import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: Tests that run in > ~1 seconds.")
    config.addinivalue_line("markers", "client: Tests that run outside the containers.")
