import pytest
from playwright.sync_api import sync_playwright


def test_cart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

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

        browser.close()
