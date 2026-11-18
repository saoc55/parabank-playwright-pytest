import pytest
from playwright.sync_api import Page, expect

from pages.open_account_page import OpenAccountPage


@pytest.fixture
def open_new_account(authenticated_page: Page) -> OpenAccountPage:
    open_account_page = OpenAccountPage(authenticated_page)
    open_account_page.goto()
    return open_account_page


class TestOpenNewAccount:
    def test_tc12_open_new_account(self, open_new_account: OpenAccountPage) -> None:
        open_new_account.open_account()
        expect(open_new_account.new_account_id).not_to_be_empty()
