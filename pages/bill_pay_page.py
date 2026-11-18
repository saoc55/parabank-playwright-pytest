from playwright.sync_api import Page


class BillPayPage:
    def __init__(self, page: Page) -> None:
        self.page = page

        # Inputs
        self.name = page.locator('input[name="payee.name"]')
        self.address = page.locator('input[name="payee.address.street"]')
        self.city = page.locator('input[name="payee.address.city"]')
        self.state = page.locator('input[name="payee.address.state"]')
        self.zip_code = page.locator('input[name="payee.address.zipCode"]')
        self.phone = page.locator('input[name="payee.phoneNumber"]')
        self.account_number = page.locator('input[name="payee.accountNumber"]')
        self.verify_account = page.locator('input[name="verifyAccount"]')
        self.amount = page.locator('input[name="amount"]')
        self.from_account_id = page.locator('select[name="fromAccountId"]')

        # Send
        self.send_payment = page.locator('input[value="Send Payment"]')

        self.bill_pay_result = page.locator("#billpayResult h1.title")

        self.validation_model = page.locator("#validationModel-name")

    def goto(self) -> None:
        self.page.goto("/parabank/billpay.htm")

    def pay_bill(
        self,
        name: str,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        phone: str,
        account: str,
        amount: str,
    ) -> None:
        self.name.fill(name)
        self.address.fill(address)
        self.city.fill(city)
        self.state.fill(state)
        self.zip_code.fill(zip_code)
        self.phone.fill(phone)
        self.account_number.fill(account)
        self.verify_account.fill(account)
        self.amount.fill(amount)

        self.from_account_id.select_option(index=0)

        self.send_payment.click()
