import allure
import pytest

from pages.main_page import MainPage
from pages.order_page import OrderPage

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

DZEN_URL_PARTS = ("dzen.ru", "yandex.ru")


@pytest.fixture(params=USERS, ids=["точка входа сверху", "точка входа снизу"])
def created_order(request, driver):
    main = MainPage(driver)
    order = OrderPage(driver)
    with allure.step("Оформляем заказ через кнопку «Заказать»"):
        main.open()
        main.click_order_button(request.param["entry_point"])
        order.fill_user_info(request.param)
        order.fill_rent_info(request.param)
        order.confirm_order()
    return main, order


class TestOrder:
    @allure.title("После успешного оформления появляется всплывающее окно заказа")
    @allure.feature("Оформление заказа")
    def test_order_success_popup_visible(self, created_order):
        _, order = created_order
        assert order.is_success_popup_visible()

    @allure.title("Клик по логотипу Самоката возвращает на главную страницу")
    @allure.feature("Навигация")
    def test_samokat_logo_opens_main_page(self, created_order):
        main, _ = created_order
        main.click_samokat_logo()
        assert MainPage.MAIN_URL in main.get_current_url()

    @allure.title("Клик по логотипу Яндекса открывает Дзен в новом окне")
    @allure.feature("Навигация")
    def test_yandex_logo_opens_dzen(self, created_order):
        main, _ = created_order
        # Возвращаемся на главную, где доступен логотип Яндекса
        main.click_samokat_logo()
        main.click_yandex_logo()
        main.switch_to_new_window()
        main.wait_url_contains_any(DZEN_URL_PARTS)
        assert any(p in main.get_current_url() for p in DZEN_URL_PARTS)
