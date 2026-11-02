import allure
from selenium.webdriver.common.by import By

from Pages.base_page import BasePage


class DashboardPage(BasePage):
    """OrangeHRM dashboard, shown after a successful login."""

    # ── Locators ─────────────────────────────────────────────
    DASHBOARD_HEADER = (By.XPATH, "//h6[text()='Dashboard']")
    USER_DROPDOWN = (By.XPATH, "//li[@class='oxd-userdropdown']")
    LOGOUT_OPTION = (By.XPATH, "//a[text()='Logout']")
    LOGGED_IN_USERNAME = (By.XPATH, "//p[@class='oxd-userdropdown-name']")
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search']")

    # ── Read methods ─────────────────────────────────────────
    def is_loaded(self):
        return self.is_visible(self.DASHBOARD_HEADER)

    def get_page_heading(self):
        return self.get_text(self.DASHBOARD_HEADER)

    def get_logged_in_username(self):
        return self.get_text(self.LOGGED_IN_USERNAME)

    # ── Action methods ───────────────────────────────────────
    @allure.step("Logout from application")
    def logout(self):
        self.click(self.USER_DROPDOWN)
        self.click(self.LOGOUT_OPTION)
        return self.wait_for_url_contains("auth/login")

    @allure.step("Navigate to module: {module_name}")
    def navigate_to(self, module_name):
        self.enter_text(self.SEARCH_INPUT, module_name)
