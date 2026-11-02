import allure
import pytest

from Pages.dashboard_page import DashboardPage


@allure.feature("Login Module")
class TestLogin:

    @pytest.mark.smoke
    @pytest.mark.login
    @allure.story("Valid login")
    @allure.title("Valid credentials redirect to dashboard")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_valid_login(self, login_page, config):
        creds = config["credentials"]
        login_page.login(creds["username"], creds["password"])
        assert login_page.is_dashboard_visible(), "Dashboard did not appear after valid login"

    @pytest.mark.regression
    @pytest.mark.login
    @allure.story("Valid login")
    @allure.title("Dashboard header is shown after valid login")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_dashboard_header_after_login(self, login_page, config):
        creds = config["credentials"]
        login_page.login(creds["username"], creds["password"])
        dashboard = DashboardPage(login_page.driver, login_page.timeout)
        assert dashboard.is_loaded(), "Dashboard header not visible"

    @pytest.mark.regression
    @pytest.mark.login
    @allure.story("Invalid login")
    @allure.title("Wrong password shows 'Invalid credentials'")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_wrong_password(self, login_page):
        login_page.login("Admin", "wrong_password")
        assert "Invalid credentials" in login_page.get_error_message()

    @pytest.mark.regression
    @pytest.mark.login
    @allure.story("Invalid login")
    @allure.title("Wrong username shows 'Invalid credentials'")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_wrong_username(self, login_page):
        login_page.login("wrong_user", "admin123")
        assert "Invalid credentials" in login_page.get_error_message()

    @pytest.mark.regression
    @pytest.mark.login
    @allure.story("Invalid login")
    @allure.title("Wrong username and password show 'Invalid credentials'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_wrong_username_and_password(self, login_page):
        login_page.login("wrong_user", "wrong_password")
        assert "Invalid credentials" in login_page.get_error_message()

    @pytest.mark.regression
    @pytest.mark.login
    @allure.story("Invalid login")
    @allure.title("Empty fields show 'Required' validation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_fields_show_required(self, login_page):
        login_page.login("", "")
        assert "Required" in login_page.get_validation_messages()
