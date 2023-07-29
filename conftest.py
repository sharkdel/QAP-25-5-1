import pytest as pytest
from selenium import webdriver


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    # Можно задавать нужный вам размер экрана
    driver.set_window_size(1080, 800)
    #driver.maximize_window()
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')
    yield driver
    driver.quit()
    