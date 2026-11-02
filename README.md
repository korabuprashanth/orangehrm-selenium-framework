# OrangeHRM Selenium Test Framework

UI automation framework for the [OrangeHRM open-source demo](https://opensource-demo.orangehrmlive.com), built with **Python, Selenium 4, pytest, and Allure**. It uses the Page Object Model, a YAML config, a shared logger, screenshot-on-failure, and CI that publishes the Allure report to GitHub Pages.

**Live report:** https://<your-username>.github.io/orangehrm-selenium-framework/

## Tech Stack
- Python 3.10+
- Selenium WebDriver 4 (Selenium Manager handles chromedriver)
- pytest
- Allure reports (allure-pytest)
- GitHub Actions for CI

## Project Structure

```
orangehrm-selenium-framework/
├── .github/workflows/allure-report.yml   CI: run tests, publish Allure to GitHub Pages
├── Config/config.yaml                    URL, browser, headless, credentials, timeouts
├── Utilities/
│   ├── config_reader.py                  Reads config.yaml into a dict
│   └── logger.py                         Console + reports/test.log
├── Pages/
│   ├── base_page.py                      Selenium wrappers, explicit waits, logging
│   ├── login_page.py                     Locators + open / login / read methods
│   └── dashboard_page.py                 Locators + is_loaded / heading / logout / navigate_to
├── Tests/
│   ├── test_login.py                     6 tests (valid login, invalid logins, empty fields)
│   └── test_dashboard.py                 4 tests
├── conftest.py                           Fixtures, --headless option, Allure env + screenshots
├── pytest.ini                            Markers and Allure output folder
├── requirements.txt
└── .gitignore
```

## Design Notes
- **Page Object Model:** Locators and page actions live in `Pages/`. Tests contain only assertions and flow.
- **BasePage:** All raw Selenium calls go through one class, which adds explicit waits and logging.
- **Allure:** Features, stories, severities, and titles label each test. Page actions are `@allure.step` so the report shows each step.
- **Failure evidence:** A failed test attaches a screenshot to its Allure result.
- **Config-driven:** Change the URL, browser, or headless mode in `Config/config.yaml`.

## Setup

```bash
git clone https://github.com/<your-username>/orangehrm-selenium-framework.git
cd orangehrm-selenium-framework

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

You need Chrome installed. You also need the [Allure CLI](https://allurereport.org/docs/install/) to view reports locally.

## Running Tests

```bash
pytest                            # run everything
pytest Tests/test_login.py        # one file
pytest -m smoke                   # by marker
pytest -k "wrong_password"        # by keyword
pytest --headless                 # no browser window
```

## Allure Report

```bash
pytest                            # writes results to reports/allure-results
allure serve reports/allure-results
```

The report includes:
- Features, stories, and severities per test
- Step-by-step actions (open page, login, logout)
- Environment info (browser, base URL, Python, OS)
- Screenshots on failed tests

### Automatic publishing

On every push to `main`, GitHub Actions runs the suite and publishes the report to GitHub Pages. To enable it:
1. Go to **Settings → Pages** and set the source to the `gh-pages` branch. It is created on the first run.
2. Open the report at `https://<your-username>.github.io/orangehrm-selenium-framework/`.

## Test Coverage

| Area | Tests | What's covered |
|---|---|---|
| Login | 6 | Valid login, dashboard header after login, wrong password, wrong username, case-sensitive username, empty fields |
| Dashboard | 4 | Page loads, heading is "Dashboard", logged-in user is Admin, logout redirects to login |

## Notes
- The OrangeHRM demo resets periodically and its credentials are public. If logins fail, check the demo site first.

## Author
**Your Name** · [LinkedIn](https://linkedin.com/in/your-profile) · [Email](mailto:you@example.com)
