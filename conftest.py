from typing import Tuple

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as OptionsChrome
from selenium.webdriver.firefox.options import Options as OptionsFirefox
from selenium.webdriver.remote.webdriver import WebDriver
# пример запуска pytest -s -v --browser_name=firefox --language=ru test_name.py
# позволяет автоматически импортировать фикстуры из данного модуля в разные тесты


# Инициализирует язык и драйвер chrome
def chrome_launch(request) -> Tuple[WebDriver, str]:
    options = OptionsChrome()
    selected_language = request.config.getoption("language")
    options.add_experimental_option('prefs', {'intl.accept_languages': selected_language})
    browser = webdriver.Chrome(options=options)
    return browser, selected_language


# Инициализирует язык и драйвер firefox
def firefox_launch(request) -> Tuple[WebDriver, str]:
    options = OptionsFirefox()
    selected_language = request.config.getoption("language")
    options.set_preference("intl.accept_languages", selected_language)
    browser = webdriver.Firefox(options=options)
    return browser, selected_language


# здесь хранятся функции для инициализации запрашиваемого браузера
supported_browsers = {
    'chrome': chrome_launch,
    'firefox': firefox_launch
}


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")
    parser.addoption('--language', action='store', default='ru',
                     help="Choose language: for example: '--language=en' or '--language=ru'")


# Проверяем есть ли запрашиваемый браузер и запускаем его либо райзим ошибку
@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("browser_name")
    if browser_name in supported_browsers:
        browser, selected_language = supported_browsers.get(browser_name)(request)
        print(f"\nstart {browser_name} browser with language={selected_language} for test..")
    else:
        joined_browsers = ', '.join(supported_browsers.keys())
        raise pytest.UsageError(f"--browser_name is invalid, supported browsers: {joined_browsers}")

    yield browser
    print("\nquit browser..")
    browser.quit()
