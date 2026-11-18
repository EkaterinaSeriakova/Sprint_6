import time
from allure import step
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage


class OrderPage(BasePage):
    FIRST_NAME = (By.XPATH, "//input[contains(@placeholder,'Имя')]")
    LAST_NAME = (By.XPATH, "//input[contains(@placeholder,'Фамилия')]")
    ADDRESS = (By.XPATH, "//input[contains(translate(@placeholder,'АДРЕСА','адреса'),'адрес')]")
    METRO_STATION = (By.XPATH, "//input[contains(@placeholder,'метро')]")
    PHONE = (By.XPATH, "//input[contains(@placeholder,'Телефон')]")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")

    DATE_FIELD = (By.XPATH, "//input[contains(@placeholder,'Когда')]")
    RENTAL_PERIOD = (By.XPATH, "//div[contains(@class, 'Dropdown-control')]")
    COLOR_BLACK = (By.XPATH, "//label[contains(text(), 'чёрный жемчуг')]")
    COLOR_GREY = (By.XPATH, "//label[contains(text(), 'серая безысходность')]")
    COMMENT = (By.XPATH, "//input[contains(@placeholder,'Комментарий')]")
    ORDER_BUTTONS = (By.XPATH, "//button[text()='Заказать']")

    CONFIRM_YES_BUTTON = (By.XPATH, "//button[text()='Да']")
    SUCCESS_HEADER = (By.XPATH, "//div[contains(@class, 'Order_ModalHeader')]")

    @step("Заполняем форму «Для кого самокат»")
    def fill_user_info(self, user):
        self.send_keys(self.FIRST_NAME, user["name"])
        self.send_keys(self.LAST_NAME, user["surname"])
        self.send_keys(self.ADDRESS, user["address"])
        self.click(self.METRO_STATION)
        self.send_keys(self.METRO_STATION, user["metro"])
        WebDriverWait(self.driver, 15).until(lambda d: d.find_elements(
            By.XPATH, "//ul[contains(@class,'select-search__options')]/li"
        ))
        option = (By.XPATH, f"//div[contains(@class,'select-search__select')]//button[contains(., '{user['metro']}')]")
        self.click(option)


        self.send_keys(self.PHONE, user["phone"])
        self.click(self.NEXT_BUTTON)

    @step("Заполняем форму «Про аренду»")
    def fill_rent_info(self, rent):
        date_input = self.find(self.DATE_FIELD)
        date_input.clear()
        date_input.send_keys(rent["date"])
        date_input.send_keys(Keys.RETURN)
        self.click(self.RENTAL_PERIOD)
        self.wait.until(lambda d: d.find_elements(
            By.XPATH, "//div[contains(@class,'Dropdown-option')]"
        ))
        self.js_click((By.XPATH, f"//div[contains(@class,'Dropdown-option')][contains(., '{rent['period']}')]"))
        if rent.get("color") == "black":
            self.click(self.COLOR_BLACK)
        elif rent.get("color") == "grey":
            self.click(self.COLOR_GREY)
        if rent.get("comment"):
            self.send_keys(self.COMMENT, rent["comment"])
        buttons = self.find_all(self.ORDER_BUTTONS)
        self.driver.execute_script("arguments[0].click();", buttons[-1])

    @step("Подтверждаем заказ")
    def confirm_order(self):
        self.click(self.CONFIRM_YES_BUTTON)

    @step("Проверяем всплывающее окно об успешном заказе")
    def is_success_popup_visible(self):
        return self.find(self.SUCCESS_HEADER).is_displayed()
