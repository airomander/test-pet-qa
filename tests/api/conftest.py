import logging

import pytest

from api_clients.reqres_client import ReqResClient
from config.config import config

logger = logging.getLogger(__name__)


@pytest.fixture
def api_client() -> ReqResClient:
    return ReqResClient()


def pytest_collection_modifyitems(session, items) -> None:
    """Skip tests that need SAUCE_REQRES_API_KEY if it is not set."""
    if not config.reqres_api_key:
        logger.warning("SAUCE_REQRES_API_KEY not set — skipping requires_api_key tests")
        for item in items:
            if item.get_closest_marker("requires_api_key"):
                item.add_marker(pytest.mark.skip(reason="SAUCE_REQRES_API_KEY not set"))
