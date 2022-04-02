import os
from urllib.error import HTTPError
from urllib.request import urlopen

import pytest
from utils import DefaultApiValues, RestApiDefinition

SERVER_HOST_NAME = "localhost"
REST_PORT = os.getenv("REST_PORT", DefaultApiValues.REST_PORT)


@pytest.mark.client
@pytest.mark.parametrize("id", [-1])
def test_client_get_invocation_info_404(id):
    try:
        urlopen(
            f"http://{SERVER_HOST_NAME}:{REST_PORT}/{RestApiDefinition.GET_INVOCATION_INFO}/{id}"
        )
    except HTTPError as ex:
        assert ex.code == 404
