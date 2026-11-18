import pytest
from playwright.sync_api import Page, expect

from pages.bill_pay_page import BillPayPage


@pytest.fixture
def bill_payment_page(authenticated_page: Page) -> BillPayPage:
    page_object = BillPayPage(authenticated_page)
    page_object.goto()
    return page_object


class TestBillPayment:
    def test_tc08_bill_pay_form_submits_successfully_with_valid_data(
        self, bill_payment_page: BillPayPage
    ) -> None:
        bill_payment_page.pay_bill(
            name="Test Payee",
            address="123 Main St",
            city="Springfield",
            state="OH",
            zip_code="12345",
            phone="555-1234",
            account="12456",
            amount="25",
        )

        expect(bill_payment_page.bill_pay_result).to_have_text("Bill Payment Complete")

    def test_tc09_bill_pay_with_missing_payee_name_shows_validation_error(
        self, bill_payment_page: BillPayPage
    ) -> None:
        bill_payment_page.send_payment.click()

        expect(bill_payment_page.validation_model).to_be_visible()
