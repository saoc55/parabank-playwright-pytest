from playwright.sync_api import Page


class TransferFundsPage:
    def __init__(self, page: Page) -> None:
        self.page = page

        # Form inputs
        self.amount_input = page.locator("#amount")
        self.from_account = page.locator("#fromAccountId")
        self.to_account = page.locator("#toAccountId")
        self.transfer_button = page.locator('input[value="Transfer"]')

        # Success result
        self.success_title = page.locator("#showResult h1.title")
        self.amount_result = page.locator("#amountResult")
        self.from_account_result = page.locator("#fromAccountIdResult")
        self.to_account_result = page.locator("#toAccountIdResult")

        # Validation error (amount field)
        self.error_panel = page.locator("#showError")
        self.error_panel_title = page.locator("#showError h1.title")

    def goto(self) -> None:
        self.page.goto("/parabank/transfer.htm")

    def transfer(self, amount: str, from_index: int = 0, to_index: int = 1) -> None:
        """Fill and submit the transfer form.

        Args:
            amount: Dollar amount as string, e.g. "50".
            from_index: Option index for the from account (default 0).
            to_index: Option index for the to account (default 1).
        """
        self.from_account.select_option(index=from_index)
        self.to_account.select_option(index=to_index)
        self.amount_input.fill(amount)
        self.transfer_button.click()
        self.success_title.wait_for(state="visible")
