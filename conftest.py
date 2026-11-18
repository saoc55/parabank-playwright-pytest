"""Shared fixtures. pytest discovers this file automatically, so tests never import it."""

from collections.abc import Iterator

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from utils.test_data import VALID_USER


@pytest.fixture
def authenticated_page(page: Page) -> Iterator[Page]:
    """Logs in before each test that requests it, then hands the logged in page over."""
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(VALID_USER.username, VALID_USER.password)
    # wait for post login landing: Accounts Overview
    page.wait_for_url("**/overview.htm", timeout=10_000)

    yield page  # code after yield runs as teardown
