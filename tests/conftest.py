import pytest
from selene import browser
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope='function')
def setup_browser():
    chrome_options = Options()

    # Основные опции для скрытия автоматизации
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Дополнительные опции
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")

    # Конфигурация Selene
    browser.config.driver_options = chrome_options
    browser.config.base_url = "https://example.com"  # опционально

    # Скрипты для маскировки
    #browser.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    yield browser
    browser.quit()