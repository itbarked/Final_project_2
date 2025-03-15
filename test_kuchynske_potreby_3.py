import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="module")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

def test_cart_count(page):
    url="https://www.kuchynskepotreby.cz/bloky-listy-na-noze/"
    page.goto(url)

    reject_cookies_button = page.locator("#xx-cookies-plugin > div.cp-content-wrap.no-transition > div > p:nth-child(5) > a")
    reject_cookies_button.click()

    product_1 = page.locator("button:has-text('Koupit')").first
    product_1.click()
    page.keyboard.press("Escape")

    product_2 = page.locator("button:has-text('Koupit')").nth(1)
    product_2.click()
    page.keyboard.press("Escape")

    cart = page.locator("#basket_cena")
    cart.click()
    page.wait_for_load_state("networkidle", timeout=30000)

    No_of_products_in_basket = page.inner_text('#basket_pocet')
    assert No_of_products_in_basket == "2", f"V košíku by měly být 2 různé produkty, ale je jich tam: {No_of_products_in_basket}"

def test_cart_sum(page):
    url="https://www.kuchynskepotreby.cz/nakupni-kosik/"
    page.goto(url)
    
    cart_wrap = page.query_selector("#content > div.basket-wrap") 
    product_1_price = cart_wrap.query_selector("#basketa > table > tbody > tr:nth-child(1) > td.price").inner_text()
    product_2_price = cart_wrap.query_selector("#basketa > table > tbody > tr:nth-child(2) > td.price").inner_text()
    price_total = cart_wrap.query_selector("#basketa > div.basket-total-price > strong").inner_text()

    product_1_price = float(product_1_price.replace("Kč", "").strip())
    product_2_price = float(product_2_price.replace("Kč", "").strip())
    price_total = float(price_total.replace("Kč", "").strip())

    expected_total = product_1_price + product_2_price
    assert expected_total == price_total, f"Součet cen produktů ({expected_total}) není rovný celkové ceně ({price_total})"
