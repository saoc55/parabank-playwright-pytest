from playwright.sync_api import Page


class OpenAccountPage:
    def __init__(self, page: Page) -> None:
        self.page = page

        # Form inputs
        self.account_type = page.locator("#type")
        self.from_account = page.locator("#fromAccountId")
        self.open_account_button = page.locator('input[value="Open New Account"]')

        # Result containers
        self.success_container = page.locator("#openAccountResult")
        self.new_account_id = page.locator("#newAccountId")
        self.error_container = page.locator("#openAccountError")

    def goto(self) -> None:
        self.page.goto("/parabank/openaccount.htm")
        # the from account <select> is filled by AJAX; wait until it has an option
        self.from_account.locator("option").first.wait_for(state="attached")

    def open_account(self, account_type: str = "0") -> None:
        """account_type: "0" = CHECKING, "1" = SAVINGS (option values of #type)."""
        self.account_type.select_option(account_type)
        self.open_account_button.click()
        self.success_container.wait_for(state="visible", timeout=15_000)
