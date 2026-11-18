import re

from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from utils.test_data import INVALID_USER, VALID_USER


class TestAuthentication:
    def test_tc01_valid_login_redirects_to_account_overview(self, page: Page) -> None:
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(VALID_USER.username, VALID_USER.password)
        expect(page).to_have_url(re.compile(r"overview"))

    def test_tc02_invalid_credentials_show_error(self, page: Page) -> None:
        login_page = LoginPage(page)
        login_page.goto()
        login_page.login(INVALID_USER.username, INVALID_USER.password)
        error = login_page.get_error_message()
        assert "The username and password could not be verified" in (error or "")
