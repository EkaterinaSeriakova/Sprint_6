import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 10


class BasePage:
    MAIN_URL = "https://qa-scooter.praktikum-services.ru/"
    COOKIE_BUTTON = (By.ID, "rcc-confirm-button")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    @allure.step("Открываем страницу: {path}")
    def open(self, path=""):
        self.driver.get(self.MAIN_URL + path)
        self.close_cookie_banner_if_visible()

    @allure.step("Закрываем баннер про куки, если он появился")
    def close_cookie_banner_if_visible(self):
        try:
            WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(self.COOKIE_BUTTON)
            ).click()
        except TimeoutException:
            pass

    @allure.step("Ждём видимости элемента {locator}")
    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Ждём появления списка элементов {locator}")
    def get_elements(self, locator, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )
        return self.driver.find_elements(*locator)


    @allure.step("Кликаем по элементу {locator}")
    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    @allure.step("Заполняем поле {locator} текстом «{text}»")
    def send_keys(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Скроллим к элементу {locator}")
    def scroll_to(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

    @allure.step("Кликаем по элементу {locator} через JavaScript")
    def js_click(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Кликаем через JavaScript по элементу с индексом {index} из списка {locator}")
    def js_click_from_list(self, locator, index):
        elements = self.get_elements(locator)
        self.driver.execute_script("arguments[0].click();", elements[index])

    @allure.step("Переключаемся на новое окно")
    def switch_to_new_window(self):
        self.wait.until(EC.number_of_windows_to_be(2))
        new_window = [
            w for w in self.driver.window_handles
            if w != self.driver.current_window_handle
        ][0]
        self.driver.switch_to.window(new_window)

    @allure.step("Ждём, пока адрес страницы будет содержать один из фрагментов: {parts}")
    def wait_url_contains_any(self, parts):
        self.wait.until(lambda d: any(p in d.current_url for p in parts))

    @allure.step("Получаем текущий адрес страницы")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Подставляем значения {args} в локатор {locator}")
    def format_locator(self, locator, *args):
        how, what = locator
        return (how, what.format(*args))

    @allure.step("Заполняем поле {locator} текстом «{text}» и нажимаем Enter")
    def send_keys_and_enter(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text, Keys.RETURN)
    
