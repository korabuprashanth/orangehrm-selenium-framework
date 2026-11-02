from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Utilities.logger import get_logger


class BasePage:
    """Wraps raw Selenium calls with explicit waits and logging.

    Page classes call these helpers and never call find_element directly.
    """

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.log = get_logger()

    def _wait(self, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout)

    def open_url(self, url):
        self.log.info(f"Open → {url}")
        self.driver.get(url)

    def click(self, locator):
        self.log.info(f"Click → {locator}")
        self._wait().until(EC.element_to_be_clickable(locator)).click()

    def enter_text(self, locator, text):
        self.log.info(f"Type '{text}' → {locator}")
        element = self._wait().until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        self.log.info(f"Get text → {locator}")
        element = self._wait().until(EC.visibility_of_element_located(locator))
        return element.text.strip()

    def get_all_texts(self, locator, timeout=None):
        """Return the text of every matching element, or [] if none appear."""
        try:
            elements = self._wait(timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            return []
        return [e.text.strip() for e in elements if e.text.strip()]

    def is_visible(self, locator, timeout=None):
        try:
            self._wait(timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    def wait_for_visible(self, locator, timeout=None):
        """Block until the element is visible. Raises TimeoutException if it never appears."""
        return self._wait(timeout).until(EC.visibility_of_element_located(locator))

    def wait_for_url_contains(self, fragment, timeout=None):
        try:
            self._wait(timeout).until(EC.url_contains(fragment))
            return True
        except TimeoutException:
            return False

    def get_url(self):
        return self.driver.current_url
