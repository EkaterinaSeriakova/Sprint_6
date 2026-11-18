import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class OrderPage(BasePage):
    FIRST_NAME = (By.XPATH, "//input[contains(@placeholder,'Имя')]")
    LAST_NAME = (By.XPATH, "//input[contains(@placeholder,'Фамилия')]")
    ADDRESS = (By.XPATH, "//input[contains(translate(@placeholder,'АДРЕСА','адреса'),'адрес')]")
    METRO_STATION = (By.XPATH, "//input[contains(@placeholder,'метро')]")
    METRO_OPTIONS = (By.XPATH, "//ul[contains(@class,'select-search__options')]/li")
    METRO_OPTION_TEXT = (By.XPATH, "//div[contains(@class,'select-search__select')]//button[contains(., '{}')]")
    PHONE = (By.XPATH, "//input[contains(@placeholder,'Телефон')]")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")

    DATE_FIELD = (By.XPATH, "//input[contains(@placeholder,'Когда')]")
    RENTAL_PERIOD = (By.XPATH, "//div[contains(@class, 'Dropdown-control')]")
    DROPDOWN_OPTIONS = (By.XPATH, "//div[contains(@class,'Dropdown-option')]")
    DROPDOWN_OPTION_TEXT = (By.XPATH, "//div[contains(@class,'Dropdown-option')][contains(., '{}')]")
    COLOR_BLACK = (By.XPATH, "//label[contains(text(), 'чёрный жемчуг')]")
    COLOR_GREY = (By.XPATH, "//label[contains(text(), 'серая безысходность')]")
    COMMENT = (By.XPATH, "//input[contains(@placeholder,'Комментарий')]")
    ORDER_BUTTONS = (By.XPATH, "//button[text()='Заказать']")

    CONFIRM_YES_BUTTON = (By.XPATH, "//button[text()='Да']")
    SUCCESS_HEADER = (By.XPATH, "//div[contains(@class, 'Order_ModalHeader')]")

    @allure.step("Выбираем станцию метро: {metro}")
    def select_metro(self, metro):
        self.click(self.METRO_STATION)
        self.send_keys(self.METRO_STATION, metro)
        self.get_elements(self.METRO_OPTIONS, timeout=15)
        self.click(self.format_locator(self.METRO_OPTION_TEXT, metro))

    @allure.step("Заполняем форму «Для кого самокат»")
    def fill_user_info(self, user):
        self.send_keys(self.FIRST_NAME, user["name"])
        self.send_keys(self.LAST_NAME, user["surname"])
        self.send_keys(self.ADDRESS, user["address"])
        self.select_metro(user["metro"])
        self.send_keys(self.PHONE, user["phone"])
        self.click(self.NEXT_BUTTON)

    @allure.step("Выбираем цвет самоката: {color}")
    def select_color(self, color):
        colors = {"black": self.COLOR_BLACK, "grey": self.COLOR_GREY}
        if color in colors:
            self.click(colors[color])

    @allure.step("Заполняем форму «Про аренду»")
    def fill_rent_info(self, rent):
        self.send_keys_and_enter(self.DATE_FIELD, rent["date"])
        self.click(self.RENTAL_PERIOD)
        self.get_elements(self.DROPDOWN_OPTIONS)
        self.js_click(self.format_locator(self.DROPDOWN_OPTION_TEXT, rent["period"]))
        self.select_color(rent.get("color"))
        if rent.get("comment"):
            self.send_keys(self.COMMENT, rent["comment"])
        self.js_click_from_list(self.ORDER_BUTTONS, -1)

    @allure.step("Подтверждаем заказ")
    def confirm_order(self):
        self.click(self.CONFIRM_YES_BUTTON)

    @allure.step("Проверяем всплывающее окно об успешном заказе")
    def is_success_popup_visible(self):
        self.find(self.SUCCESS_HEADER)
        return True
