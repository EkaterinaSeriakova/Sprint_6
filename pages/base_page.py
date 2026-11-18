from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    MAIN_URL = "https://qa-scooter.praktikum-services.ru/"
    COOKIE_BUTTON = (By.ID, "rcc-confirm-button")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, path=""):
        self.driver.get(self.MAIN_URL + path)
        # Закрываем куки-баннер, если он появился — иначе он перекрывает элементы
        try:
            WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(self.COOKIE_BUTTON)
            ).click()
        except TimeoutException:
            pass

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        self.wait.until(EC.presence_of_all_elements_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def send_keys(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def scroll_to(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

    def js_click(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", element)

    def switch_to_new_window(self):
        self.wait.until(EC.number_of_windows_to_be(2))
        new_window = [
            w for w in self.driver.window_handles
            if w != self.driver.current_window_handle
        ][0]
        self.driver.switch_to.window(new_window)
