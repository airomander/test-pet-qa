import logging

import pytest
import requests

from api_clients.reqres_client import ReqResClient
from config.config import config

logger = logging.getLogger(__name__)


@pytest.fixture
def api_client() -> ReqResClient:
    return ReqResClient()


def pytest_collection_modifyitems(session, config_obj, items):
    api_key = config.reqres_api_key
    if not api_key:
        _skip_all(items, "SAUCE_REQRES_API_KEY is not configured")
        return

    try:
        resp = requests.get(
            "https://reqres.in/api/users/2",
            headers={"x-api-key": api_key},
            timeout=10,
        )
        if resp.status_code in (401, 403, 429):
            _skip_all(items, f"ReqRes API returned {resp.status_code} — check your API key")
    except requests.RequestException as e:
        _skip_all(items, f"ReqRes API unreachable: {e}")


def _skip_all(items, reason: str) -> None:
    logger.warning(f"Skipping API tests: {reason}")
    for item in items:
        item.add_marker(pytest.mark.skip(reason=reason))
