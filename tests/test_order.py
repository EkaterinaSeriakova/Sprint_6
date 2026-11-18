import allure
import pytest

from pages.main_page import MainPage
from pages.order_page import OrderPage
from selenium.webdriver.support.ui import WebDriverWait


USERS = [
    {
        "entry_point": "top",
        "name": "Олег", "surname": "Перчаткин", "address": "ул. Карбышева, 5",
        "metro": "Сокольники", "phone": "+79991112233",
        "date": "25.11.2026", "period": "двое суток",
        "color": "black", "comment": "Позвоните за час",
    },
    {
        "entry_point": "bottom",
        "name": "Мария", "surname": "Кошкина", "address": "ул. Рубинштейна, 12",
        "metro": "Черкизовская", "phone": "+79217778855",
        "date": "30.11.2026", "period": "сутки",
        "color": "grey", "comment": "",
    },
]


class TestOrder:
    @allure.title("Позитивный флоу заказа самоката: точка входа «{user[entry_point]}»")
    @allure.feature("Оформление заказа")
    @pytest.mark.parametrize("user", USERS)
    def test_order_success_flow(self, driver, user):
        main = MainPage(driver)
        order = OrderPage(driver)

        main.open()
        main.click_order_button(user["entry_point"])
        order.fill_user_info(user)
        order.fill_rent_info(user)
        order.confirm_order()

        assert order.is_success_popup_visible()

        # Проверяем логотип Самоката — возврат на главную
        main.click_samokat_logo()
        assert "qa-scooter.praktikum-services.ru" in driver.current_url

        # Проверяем логотип Яндекса — редирект в Дзен в новом окне
        main.click_yandex_logo()
        main.switch_to_new_window()
        WebDriverWait(driver, 10).until(
            lambda d: "dzen.ru" in d.current_url or "yandex.ru" in d.current_url
        )
        assert "dzen.ru" in driver.current_url or "yandex.ru" in driver.current_url


