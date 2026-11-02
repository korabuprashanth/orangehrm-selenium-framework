import os
import platform
import sys

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Pages.dashboard_page import DashboardPage
from Pages.login_page import LoginPage
from Utilities.config_reader import ConfigReader

ALLURE_RESULTS_DIR = os.path.join(os.path.dirname(__file__), "reports", "allure-results")


# ── CLI options ──────────────────────────────────────────────
def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run Chrome headless (used on CI). Overrides config headless: false.",
    )


# ── Store each phase's result on the test item ──────────────
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


# ── Environment info shown in the Allure report ─────────────
def pytest_sessionfinish(session, exitstatus):
    if not os.path.isdir(ALLURE_RESULTS_DIR):
        return
    config = ConfigReader().get()
    env = {
        "Browser": config.get("browser", "chrome"),
        "Headless": str(config.get("headless", False)),
        "Base.URL": config.get("base_url", ""),
        "Python": platform.python_version(),
        "OS": platform.platform(),
    }
    with open(os.path.join(ALLURE_RESULTS_DIR, "environment.properties"), "w") as f:
        for key, value in env.items():
            f.write(f"{key}={value}\n")


# ── Fixtures ─────────────────────────────────────────────────
@pytest.fixture(scope="session")
def config():
    return ConfigReader().get()


@pytest.fixture
def driver(config, request):
    browser = config.get("browser", "chrome")
    headless = request.config.getoption("--headless") or config.get("headless", False)

    if browser != "chrome":
        raise ValueError(f"Unsupported browser: {browser}")

    options = Options()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

    drv = webdriver.Chrome(options=options)  # Selenium Manager fetches chromedriver
    if not headless:
        drv.maximize_window()

    yield drv
    drv.quit()


@pytest.fixture
def login_page(driver, config):
    page = LoginPage(driver, timeout=config.get("timeout", 10))
    page.open(config["base_url"])
    return page


@pytest.fixture
def logged_in(login_page, config):
    creds = config["credentials"]
    login_page.login(creds["username"], creds["password"])
    dashboard = DashboardPage(login_page.driver, timeout=config.get("timeout", 10))
    assert dashboard.is_loaded(), "Setup failed: dashboard did not load after login"
    return dashboard


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, driver):
    """Attach a screenshot to the Allure report when a test fails."""
    yield
    report = getattr(request.node, "rep_call", None)
    if report is not None and report.failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Failure screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
