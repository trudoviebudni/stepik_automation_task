import time

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

link = 'http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/'


def test_product_page_contains_add_to_cart_button(browser):
    browser.get(link)
    time.sleep(30)
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#add_to_basket_form button'))
        )
    except TimeoutException:
        assert False, "TimeoutException: Add to cart button is not found on the page"

