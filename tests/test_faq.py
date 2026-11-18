import allure
import pytest

from pages.main_page import MainPage

FAQ_DATA = [
    (0, "Сутки — 400 рублей. Оплата курьеру — наличными или картой."),
    (1, "Пока что у нас так: один заказ — один самокат."),
    (2, "Допустим, вы оформляете заказ на 8 мая."),
    (3, "Только начиная с завтрашнего дня."),
    (4, "Пока что нет!"),
    (5, "Самокат приезжает к вам с полной зарядкой."),
    (6, "Да, пока самокат не привезли."),
    (7, "Да, обязательно. Всем самокатов!"),
]


class TestFaq:
    @allure.title("Вопросы о важном: вопрос №{index} раскрывает ответ")
    @allure.feature("Раздел «Вопросы о важном»")
    @pytest.mark.parametrize("index, expected_text", FAQ_DATA)
    def test_faq_answer_opens(self, driver, index, expected_text):
        page = MainPage(driver)
        page.open()
        page.click_faq_question(index)
        actual_text = page.get_faq_answer_text(index)
        assert expected_text in actual_text
