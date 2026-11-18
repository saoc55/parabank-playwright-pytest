"""Shared fixtures. pytest discovers this file automatically, so tests never import it."""

from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Route

from pages.login_page import LoginPage
from utils.test_data import VALID_USER

# ParaBank sits behind Cloudflare, which rate limits bursts of requests (HTTP 429, Error 1015).
# Two measures keep the suite under that limit:
#   1. image, font and media requests are dropped (no test asserts on them)
#   2. the login runs once per browser, and every test reuses that session's cookies
BLOCKED_RESOURCE_TYPES = {"image", "font", "media"}


def _block_static_assets(route: Route) -> None:
    if route.request.resource_type in BLOCKED_RESOURCE_TYPES:
        route.abort()
    else:
        route.continue_()


@pytest.fixture
def context(new_context: Callable[..., BrowserContext]) -> BrowserContext:
    """Overrides pytest-playwright's `context`: same fresh, logged out context, minus static assets."""
    ctx = new_context()
    ctx.route("**/*", _block_static_assets)
    return ctx


@pytest.fixture(scope="session")
def auth_storage_state(
    browser: Browser, browser_context_args: dict[str, Any], tmp_path_factory: pytest.TempPathFactory
) -> Path:
    """Logs in once per browser and saves the session cookies to a JSON file."""
    args = {k: v for k, v in browser_context_args.items() if k != "record_video_dir"}
    ctx = browser.new_context(**args)
    ctx.route("**/*", _block_static_assets)
    page = ctx.new_page()

    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(VALID_USER.username, VALID_USER.password)
    page.wait_for_url("**/overview.htm", timeout=10_000)

    state_file = tmp_path_factory.mktemp("auth") / f"{browser.browser_type.name}.json"
    ctx.storage_state(path=state_file)
    ctx.close()
    return state_file


@pytest.fixture
def authenticated_page(
    new_context: Callable[..., BrowserContext], auth_storage_state: Path
) -> Page:
    """A fresh page whose context already carries the logged in session. Tests navigate from here."""
    ctx = new_context(storage_state=auth_storage_state)
    ctx.route("**/*", _block_static_assets)
    return ctx.new_page()
