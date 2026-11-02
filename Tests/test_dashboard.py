import allure
import pytest


@allure.feature("Dashboard Module")
class TestDashboard:

    @pytest.fixture(autouse=True)
    def setup(self, logged_in):
        # logged_in logs in and returns a DashboardPage
        self.page = logged_in

    @pytest.mark.smoke
    @pytest.mark.dashboard
    @allure.title("Dashboard loads after login")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_dashboard_loads(self):
        assert self.page.is_loaded(), "Dashboard did not load after login"

    @pytest.mark.regression
    @pytest.mark.dashboard
    @allure.title("Dashboard heading text is 'Dashboard'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_dashboard_heading(self):
        heading = self.page.get_page_heading()
        assert heading == "Dashboard", f"Expected 'Dashboard', got '{heading}'"

    @pytest.mark.smoke
    @pytest.mark.dashboard
    @allure.title("Logout redirects to login page")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_logout(self):
        self.page.logout()
        assert "login" in self.page.get_url().lower(), "Not redirected to login page after logout"

    @pytest.mark.regression
    @pytest.mark.dashboard
    @allure.title("Logged-in user name is displayed")
    @allure.severity(allure.severity_level.NORMAL)
    def test_logged_in_user(self):
        username = self.page.get_logged_in_username()
        assert username, "No logged-in user name is displayed"