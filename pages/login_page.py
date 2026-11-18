from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page

        # Locators
        self.username_input = page.locator('input[name="username"]')
        self.password_input = page.locator('input[name="password"]')
        self.login_button = page.locator('input[value="Log In"]')
        self.error_message = page.locator(".error")

    def goto(self) -> None:
        self.page.goto("/parabank/index.htm")

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self) -> str | None:
        return self.error_message.text_content()
