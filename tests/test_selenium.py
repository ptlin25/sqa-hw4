import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service

from pages.selenium.nav_bar import NavBar
from pages.selenium.list_page import ListPage
from pages.selenium.detail_page import DetailPage
from pages.selenium.cart_page import CartPage

from selenium import webdriver


BROWSER = "firefox"
USERNAME = "demoblaze"
PASSWORD = "demoblaze"
PRODUCT_ONE_URL = "https://www.demoblaze.com/prod.html?idp_=1"


def _get_driver(browser="chrome"):
    if browser in ["chrome", "chromium"]:
        options = ChromeOptions()
        options.add_argument("--headless=new")
        return webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--headless")
        service = Service(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    d = _get_driver(browser[0])
    yield d
    d.quit()

@pytest.fixture
def clear_cart(driver):
    _clear(driver)
    yield
    _clear(driver)


def _clear(driver):
    nav_bar = NavBar(driver)
    nav_bar.open()
    login_modal = nav_bar.click_login()
    login_modal.login(USERNAME, PASSWORD)
    nav_bar.logout()

def _add_product_one_to_cart(driver):
    driver.get(PRODUCT_ONE_URL)
    detail = DetailPage(driver)
    title = detail.get_title()
    detail.add_to_cart()
    detail.accept_cart_alert()
    return title


def test_login_shows_username_and_closes_modal(driver):
    # Arrange
    nav_bar = NavBar(driver)
    nav_bar.open()
    login_modal = nav_bar.click_login()

    # Act
    login_modal.login(USERNAME, PASSWORD)

    # Assert
    assert nav_bar.is_username_shown(USERNAME)
    assert login_modal.is_open() == False


def test_logout_clears_user_state_and_shows_login_link(driver):
    # Arrange
    nav_bar = NavBar(driver)
    nav_bar.open()
    login_modal = nav_bar.click_login()
    login_modal.login(USERNAME, PASSWORD)

    # Act
    nav_bar.logout()

    # Assert
    assert nav_bar.is_username_shown(USERNAME) == False
    assert nav_bar.is_visible(nav_bar.LOG_IN_LINK)


def test_contact_form_submission_shows_alert(driver):
    # Arrange
    nav_bar = NavBar(driver)
    nav_bar.open()
    contact_modal = nav_bar.click_contact()

    # Act
    contact_modal.submit()

    # Assert
    assert contact_modal.accept_alert_if_show()


def test_product_list_loads(driver):
    # Arrange + Act
    list_page = ListPage(driver)
    list_page.open()

    # Assert
    assert list_page.are_n_products_shown(n=9)


def test_product_details_url_title_and_price_match_tile(driver):
    # Arrange
    list_page = ListPage(driver)
    list_page.open()
    list_page.are_n_products_shown(n=1)
    tile_name, tile_price = list_page.get_first_tile_info()

    # Act
    detail = list_page.click_first_product()

    # Assert
    assert "prod.html" in driver.current_url
    assert detail.get_title() == tile_name
    assert tile_price in detail.get_price()


def test_monitors_category_filters_product_list(driver):
    # Arrange
    list_page = ListPage(driver)
    list_page.open()
    list_page.are_n_products_shown(n=9)
    original_names = list_page.get_product_names()

    # Act
    list_page.click_monitors_category()
    list_page.wait_for_products_to_change(original_names)

    # Assert
    monitor_names = list_page.get_product_names()
    assert len(monitor_names) > 0
    expected = {"Apple monitor 24", "ASUS Full HD"}
    for monitor_name in monitor_names:
        assert monitor_name in expected


def test_add_to_cart_shows_alert_and_item_appears_in_cart(driver, clear_cart):
    # Arrange
    driver.get(PRODUCT_ONE_URL)
    pp = DetailPage(driver)

    # Act
    pp.add_to_cart()
    
    # Assert
    alert_text = pp.accept_cart_alert()
    cart = CartPage(driver)
    cart.open()
    cart.wait_for_table()
    cart.wait_for_at_least_one_row()
    assert alert_text is not None
    assert len(cart.get_product_names()) == 1



def test_cart_page_renders_table_with_added_product(driver, clear_cart):
    # Arrange
    product_title = _add_product_one_to_cart(driver)

    # Act
    cart = CartPage(driver)
    cart.open()
    cart.wait_for_table()
    cart.wait_for_at_least_one_row()

    # Assert
    assert cart.is_product_present(product_title)



def test_place_order_shows_confirmation_with_id_and_amount(driver, clear_cart):
    # Arrange
    _add_product_one_to_cart(driver)
    cart = CartPage(driver)
    cart.open()
    cart.wait_for_table()
    cart.wait_for_at_least_one_row()
    order_modal = cart.click_place_order()

    # Act
    order_modal.fill_order_form()
    order_modal.wait_for_confirmation()
    details = order_modal.get_confirmation_details()

    # Assert confirmation contains a valid order ID and amount
    assert "Id:" in details
    assert "Amount:" in details


def test_remove_product_from_cart(driver, clear_cart):
    # Arrange
    product_title = _add_product_one_to_cart(driver)
    cart = CartPage(driver)
    cart.open()
    cart.wait_for_table()
    cart.wait_for_at_least_one_row()

    # Act
    cart.delete_product(product_title)

    # Assert
    assert cart.wait_for_product_removed(product_title)
    assert not cart.is_product_present(product_title)


def test_create_account_then_login_with_new_credentials(driver):
    # Arrange
    new_username = f"test_user{int(time.time())}"
    new_password = "Test1234!"

    nav_bar = NavBar(driver)
    nav_bar.open()
    signup_modal = nav_bar.click_signup()
    signup_modal.register(new_username, new_password)
    alert_text = signup_modal.accept_alert()
    login_modal = nav_bar.click_login()

    # Act
    login_modal.login(new_username, new_password)

    # Assert
    assert alert_text is not None
    assert nav_bar.is_username_shown(new_username)


def test_pagination_next_then_previous_returns_original_products(driver):
    # Arrange
    list_page = ListPage(driver)
    list_page.open()
    # if you click next and then previous, the products are rearranged into a
    # different order
    list_page.click_next()
    list_page.click_prev()

    # Act
    page1_names = list_page.get_product_names()
    list_page.click_next()
    page2_names = list_page.get_product_names()
    list_page.click_prev()
    restored_names = list_page.get_product_names()

    # Assert
    assert len(page1_names) > 0
    assert set(page2_names) != set(page1_names)
    assert set(restored_names) == set(page1_names)
