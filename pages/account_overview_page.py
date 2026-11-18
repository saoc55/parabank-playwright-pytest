from playwright.sync_api import Locator, Page


class AccountOverviewPage:
    def __init__(self, page: Page) -> None:
        self.page = page

        self.page_heading = page.locator("h1.title", has_text="Accounts Overview")
        self.account_table = page.locator("#accountTable")
        self.total_balance = page.locator("#accountTable tbody tr:last-child td:nth-child(2)")

    def goto(self) -> None:
        self.page.goto("/parabank/overview.htm")

    def get_account_rows(self) -> Locator:
        return self.account_table.locator("tbody tr")

    def get_total_balance(self) -> str | None:
        return self.total_balance.text_content()
