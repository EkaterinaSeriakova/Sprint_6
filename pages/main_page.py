import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class MainPage(BasePage):
    ORDER_BUTTONS = (By.XPATH, "//button[text()='Заказать']")
    SAMOKAT_LOGO = (By.XPATH, "//a[@href='/']")
    YANDEX_LOGO = (By.XPATH, "//a[@href='//yandex.ru']")
    FAQ_QUESTION = (By.XPATH, "(//div[@class='accordion__button'])[{}]")
    FAQ_ANSWER = (By.XPATH, "(//div[@class='accordion__panel'])[{}]")

    @allure.step("Разворачиваем вопрос №{index}")
    def click_faq_question(self, index):
        locator = self.format_locator(self.FAQ_QUESTION, index + 1)
        self.scroll_to(locator)
        self.js_click(locator)

    @allure.step("Читаем ответ на вопрос №{index}")
    def get_faq_answer_text(self, index):
        return self.find(self.format_locator(self.FAQ_ANSWER, index + 1)).text

    @allure.step("Кликаем «Заказать» через точку входа: {entry_point}")
    def click_order_button(self, entry_point):
        index = 0 if entry_point == "top" else -1
        self.js_click_from_list(self.ORDER_BUTTONS, index)

    @allure.step("Кликаем на логотип Самоката")
    def click_samokat_logo(self):
        self.js_click(self.SAMOKAT_LOGO)

    @allure.step("Кликаем на логотип Яндекса")
    def click_yandex_logo(self):
        self.js_click(self.YANDEX_LOGO)
