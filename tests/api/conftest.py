import pytest

from api_clients.reqres_client import ReqResClient


@pytest.fixture
def api_client() -> ReqResClient:
    return ReqResClient()
