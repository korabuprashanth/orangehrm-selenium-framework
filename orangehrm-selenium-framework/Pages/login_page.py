import allure
from selenium.webdriver.common.by import By

from Pages.base_page import BasePage


class LoginPage(BasePage):
    """OrangeHRM login screen. URL: /web/index.php/auth/login"""

    # ── Locators ─────────────────────────────────────────────
    USERNAME_FIELD = (By.NAME, "username")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    ERROR_MESSAGE = (By.XPATH, "//p[contains(@class,'oxd-alert-content-text')]")
    VALIDATION_MESSAGES = (By.XPATH, "//span[contains(@class,'oxd-input-field-error-message')]")
    DASHBOARD_TITLE = (By.XPATH, "//h6[text()='Dashboard']")

    # ── Actions ──────────────────────────────────────────────
    @allure.step("Open login page")
    def open(self, base_url):
        self.open_url(f"{base_url}/web/index.php/auth/login")
        self.wait_for_visible(self.USERNAME_FIELD)  # wait until the form is ready

    @allure.step("Login as '{username}'")
    def login(self, username, password):
        self.enter_text(self.USERNAME_FIELD, username)
        self.enter_text(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)

    # ── Read methods ─────────────────────────────────────────
    def is_dashboard_visible(self, timeout=None):
        return self.is_visible(self.DASHBOARD_TITLE, timeout)

    def get_error_message(self):
        """Text of the alert shown after a failed login, or '' if none appears."""
        messages = self.get_all_texts(self.ERROR_MESSAGE, timeout=5)
        return " ".join(messages)

    def get_validation_messages(self):
        """Field-level messages shown when a required field is empty, e.g. 'Required'."""
        return self.get_all_texts(self.VALIDATION_MESSAGES, timeout=5)
