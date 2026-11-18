from allure import step
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class MainPage(BasePage):
    ORDER_BUTTONS = (By.XPATH, "//button[text()='Заказать']")
    SAMOKAT_LOGO = (By.XPATH, "//a[@href='/']")
    YANDEX_LOGO = (By.XPATH, "//a[@href='//yandex.ru']")

    @staticmethod
    def faq_question(index):
        return (By.XPATH, f"(//div[@class='accordion__button'])[{index + 1}]")

    @staticmethod
    def faq_answer(index):
        return (By.XPATH, f"(//div[@class='accordion__panel'])[{index + 1}]")

    @step("Разворачиваем вопрос №{index}")
    def click_faq_question(self, index):
        self.scroll_to(self.faq_question(index))
        self.js_click(self.faq_question(index))


    @step("Читаем ответ на вопрос №{index}")
    def get_faq_answer_text(self, index):
        return self.find(self.faq_answer(index)).text

    @step("Кликаем «Заказать» через точку входа: {entry_point}")
    def click_order_button(self, entry_point):
        buttons = self.find_all(self.ORDER_BUTTONS)
        index = 0 if entry_point == "top" else -1
        self.driver.execute_script("arguments[0].click();", buttons[index])

    @step("Кликаем на логотип Самоката")
    def click_samokat_logo(self):
        self.js_click(self.SAMOKAT_LOGO)

    @step("Кликаем на логотип Яндекса")
    def click_yandex_logo(self):
        self.js_click(self.YANDEX_LOGO)
