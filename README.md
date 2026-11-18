# ParaBank Playwright pytest

![CI](https://github.com/saoc55/parabank-playwright-pytest/actions/workflows/playwright.yml/badge.svg)
![Playwright](https://img.shields.io/badge/Playwright-Python-45ba4b?logo=playwright)
![Python](https://img.shields.io/badge/Python-3.10+-3776ab?logo=python)
![License](https://img.shields.io/badge/License-MIT-blue)

End to end test automation framework built with Playwright for Python and pytest, targeting the [Parabank](https://parabank.parasoft.com) demo banking application. Demonstrates POM architecture, pytest fixtures, cross browser execution, and CI integration via GitHub Actions.

---

## Tech Stack

- **Playwright for Python** (sync API) — browser automation
- **pytest + pytest-playwright** — test runner and Playwright fixtures
- **pytest-xdist / pytest-rerunfailures / pytest-timeout** — workers, retries, per test timeout
- **Allure + pytest-html** — test reporting
- **GitHub Actions** — CI on every push to `main`
- **Browsers** — Chromium, Firefox

---

## Project Structure

```
├── pages/                        # Page Object Models
│   ├── login_page.py
│   ├── account_overview_page.py
│   ├── transfer_funds_page.py
│   ├── bill_pay_page.py
│   ├── find_transactions_page.py
│   └── open_account_page.py
├── tests/
│   ├── auth/test_login.py
│   ├── accounts/
│   │   ├── test_overview.py
│   │   └── test_open_account.py
│   ├── transactions/
│   │   ├── test_transfer.py
│   │   └── test_find_transactions.py
│   └── billpay/test_bill_pay.py
├── utils/test_data.py            # shared test data
├── conftest.py                   # authenticated_page fixture
├── pytest.ini                    # runner config
├── requirements.txt
└── .github/workflows/playwright.yml
```

---

## Setup

**Prerequisites:** Python 3.10+, Git

```bash
git clone https://github.com/saoc55/parabank-playwright-pytest.git
cd parabank-playwright-pytest
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium firefox
```

---

## Running Tests

```bash
# Run all tests (Chromium + Firefox, 2 workers, per pytest.ini)
pytest

# Run headed (visible browser), single worker, one browser
pytest --headed -n 0 --browser chromium

# Run a specific file / a single test
pytest tests/auth/test_login.py
pytest -k tc06

# Debug step by step with the Playwright Inspector
PWDEBUG=1 pytest -n 0 -k tc10

# Allure report
pytest
allure serve allure-results
```

Command line flags override `addopts` in `pytest.ini`; passing `--browser chromium` alone runs Chromium only.

---

## Test Coverage

| TC | Description | Module | Browsers |
|----|-------------|--------|----------|
| TC-01 | Valid login redirects to overview | Auth | Chromium, Firefox |
| TC-02 | Invalid credentials shows error | Auth | Chromium, Firefox |
| TC-03 | Accounts overview loads with account rows | Accounts | Chromium, Firefox |
| TC-04 | Total balance displays with $ sign | Accounts | Chromium, Firefox |
| TC-06 | Transfer funds completes successfully | Transactions | Chromium, Firefox |
| TC-07 | Transfer with missing amount shows server error | Transactions | Chromium, Firefox |
| TC-08 | Bill pay submits with valid payee | Transactions | Chromium, Firefox |
| TC-09 | Bill pay with missing payee shows validation error | Transactions | Chromium, Firefox |
| TC-10 | Find transactions by amount returns results | Transactions | Chromium, Firefox |
| TC-11 | Find transactions with no match shows empty table | Transactions | Chromium, Firefox |
| TC-12 | Open new checking account succeeds | Accounts | Chromium, Firefox |

---

## Key Patterns

**Page Object Model** — each page is a class with locators in `__init__` and interaction methods that encapsulate Playwright calls.

**Fixtures** — `authenticated_page` in `conftest.py` builds on pytest-playwright's `page` fixture to provide a logged in page. Each test module adds a small fixture that creates and opens its page object, replacing `beforeEach`.

**AJAX handling** — Parabank uses jQuery AJAX throughout. Page objects use `wait_for(state="attached")` and `wait_for(state="visible")` per endpoint behaviour instead of fixed sleeps.

**Data seeding** — TC-10 seeds a transaction by performing a real transfer to the target account before searching.

---

## CI

GitHub Actions runs the full suite on every push to `main` and uploads the HTML report, failure traces/videos and Allure results as a build artifact.
