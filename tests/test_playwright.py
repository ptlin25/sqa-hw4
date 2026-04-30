from playwright.sync_api import Page, expect

from pages.playwright.nav_bar import NavBar
from pages.playwright.detail_page import DetailPage
from pages.playwright.cart_page import CartPage

BASE_URL = "https://www.demoblaze.com"
USERNAME = "demoblaze"
PASSWORD = "demoblaze"
PRODUCT_ONE_URL = f"{BASE_URL}/prod.html?idp_=1"


def test_invalid_input_login_wrong_password(page: Page):
    # Category: Invalid Input
    # Arrange
    nav = NavBar(page).open()
    login_modal = nav.click_login()
    login_modal.fill_credentials(USERNAME, "definitely_wrong_password_xyz")

    # Act
    alert_text = login_modal.submit_and_capture_alert()

    # Assert
    assert "Wrong password" in alert_text
    expect(page.locator("#nameofuser")).not_to_be_visible()


def test_boundary_register_empty_username(page: Page):
    # Category: Boundary/Edge
    # Arrange
    nav = NavBar(page).open()
    signup_modal = nav.click_signup()
    signup_modal.fill_credentials("", "ValidPass1!")

    # Act
    alert_text = signup_modal.submit_and_capture_alert()

    # Assert
    assert "Please fill out" in alert_text


def test_equivalence_class_checkout_blank_name(page: Page):
    # Category: Equivalence Class
    # Arrange
    NavBar(page).open().login(USERNAME, PASSWORD)
    DetailPage(page).goto(PRODUCT_ONE_URL).add_to_cart()
    order_modal = CartPage(page).open().click_place_order()

    # Act
    alert_text = order_modal.fill(card="4111111111111111").submit_and_capture_alert()

    # Assert
    assert "Please fill out" in alert_text


def test_exception_handling_nonexistent_product_url(page: Page):
    # Category: Exception Handling
    # Arrange + Act
    detail = DetailPage(page).goto(f"{BASE_URL}/prod.html?idp_=999")
    page.wait_for_selector("h2.name", state="attached", timeout=10000)
    page.wait_for_timeout(3000)

    # Assert
    assert "prod.html" in page.url
    title_text = detail.get_raw_title()
    assert title_text == "" or title_text.lower() in ("undefined", "null")


def test_business_logic_duplicate_cart_entries(page: Page):
    # Category: Business Logic
    # Arrange
    NavBar(page).open().login(USERNAME, PASSWORD)
    detail = DetailPage(page)
    product_title = detail.goto(PRODUCT_ONE_URL).add_to_cart()
    detail.goto(PRODUCT_ONE_URL).add_to_cart()

    # Act
    product_names = CartPage(page).open().get_product_names()

    # Assert
    assert product_names.count(product_title) >= 2
