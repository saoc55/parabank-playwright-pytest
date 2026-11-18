from playwright.sync_api import Page, expect

from pages.find_transactions_page import FindTransactionsPage
from pages.transfer_funds_page import TransferFundsPage


class TestFindTransactions:
    def test_tc10_find_by_amount_returns_results(self, authenticated_page: Page) -> None:
        transfer = TransferFundsPage(authenticated_page)
        find_tx = FindTransactionsPage(authenticated_page)

        # Step 1: find out which account findtrans is watching
        find_tx.goto()
        target_account = find_tx.account_id.input_value()

        # Step 2: transfer TO that account (seeds the transaction we search for)
        transfer.goto()
        transfer.to_account.select_option(value=target_account)
        transfer.amount_input.fill("100")
        transfer.transfer_button.click()
        transfer.success_title.wait_for(state="visible")

        # Step 3: search
        find_tx.goto()
        find_tx.find_by_amount_value("100")

        assert find_tx.transaction_rows.count() > 0

    def test_tc11_no_match_shows_empty_results_table(self, authenticated_page: Page) -> None:
        find_tx = FindTransactionsPage(authenticated_page)

        find_tx.goto()
        find_tx.find_by_amount_value("99999.99")

        expect(find_tx.result_container).to_be_visible()
        assert find_tx.transaction_rows.count() == 0
