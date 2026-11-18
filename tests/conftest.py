import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    options = webdriver.FirefoxOptions()
    options.add_argument("--window-size=1920,1080")
    firefox_driver = webdriver.Firefox(options=options)
    firefox_driver.maximize_window()
    yield firefox_driver
    firefox_driver.quit()
