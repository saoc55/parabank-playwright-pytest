from playwright.sync_api import Page


class FindTransactionsPage:
    def __init__(self, page: Page) -> None:
        self.page = page

        self.account_id = page.locator("#accountId")
        self.amount = page.locator("#amount")
        self.find_by_amount = page.locator("#findByAmount")
        self.result_container = page.locator("#resultContainer")
        self.transaction_rows = page.locator("#transactionBody tr")

    def goto(self) -> None:
        self.page.goto("/parabank/findtrans.htm")

    def find_by_amount_value(self, amount: str) -> None:
        self.amount.fill(amount)
        self.find_by_amount.click()
        self.result_container.wait_for(state="visible")
