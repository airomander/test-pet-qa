import pytest

from api_clients.reqres_client import ReqResClient
from config.config import config


@pytest.fixture
def api_client() -> ReqResClient:
    return ReqResClient()


def pytest_collection_modifyitems(items):
    if not config.reqres_api_key:
        for item in items:
            if "test_auth" in item.nodeid or "test_users" in item.nodeid:
                item.add_marker(
                    pytest.mark.skip(reason="SAUCE_REQRES_API_KEY not configured")
                )
