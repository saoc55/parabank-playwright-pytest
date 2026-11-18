import re

import pytest
from playwright.sync_api import Page, expect

from pages.account_overview_page import AccountOverviewPage


@pytest.fixture
def accounts_overview(authenticated_page: Page) -> AccountOverviewPage:
    overview = AccountOverviewPage(authenticated_page)
    overview.goto()
    return overview


class TestOverview:
    def test_tc03_page_heading_is_visible_and_contains_accounts_overview(
        self, authenticated_page: Page, accounts_overview: AccountOverviewPage
    ) -> None:
        expect(authenticated_page).to_have_url(re.compile(r"overview\.htm"))
        expect(accounts_overview.page_heading).to_be_visible()
        expect(accounts_overview.page_heading).to_contain_text("Accounts Overview")

    def test_tc03_account_table_is_visible(self, accounts_overview: AccountOverviewPage) -> None:
        rows = accounts_overview.get_account_rows()
        expect(rows).not_to_have_count(0)

    def test_tc04_total_balance_is_visible_and_contains_dollar_sign(
        self, accounts_overview: AccountOverviewPage
    ) -> None:
        total = accounts_overview.get_total_balance()
        assert "$" in (total or "")
