import pytest
from playwright.sync_api import Page, expect

from pages.transfer_funds_page import TransferFundsPage


@pytest.fixture
def transfer_page(authenticated_page: Page) -> TransferFundsPage:
    page_object = TransferFundsPage(authenticated_page)
    page_object.goto()
    return page_object


class TestTransferFunds:
    def test_tc06_transfer_funds_succeeds_and_shows_confirmation(
        self, transfer_page: TransferFundsPage
    ) -> None:
        transfer_page.transfer("50")

        expect(transfer_page.success_title).to_be_visible()
        expect(transfer_page.success_title).to_have_text("Transfer Complete!")
        expect(transfer_page.amount_result).to_have_text("$50.00")

    def test_tc07_transfer_with_empty_amount_shows_validation_error(
        self, transfer_page: TransferFundsPage
    ) -> None:
        # Submit without filling the amount field
        transfer_page.transfer_button.click()

        expect(transfer_page.error_panel).to_be_visible()
