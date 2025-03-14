import pytest
from playwright.sync_api import sync_playwright


def test_cart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        url="https://www.kuchynskepotreby.cz/"
        page.goto(url)

        reject_cookies_button = page.locator("#xx-cookies-plugin > div.cp-content-wrap.no-transition > div > p:nth-child(5) > a")
        reject_cookies_button.click()

        product_1 = page.locator("button:has-text('Koupit')").first
        product_1.click()
        page.wait_for_selector(".fancybox-slide fancybox-slide--current fancybox-slide--html fancybox-slide--complete") 
        pokracovat_ve_vyberu_button = page.locator(".special_submit spec_l")

        product_2 = page.locator("button:has-text('Koupit')").nth(1).click()
        page.wait_for_selector(".popup_body fancybox-content")
        pokracovat_ve_vyberu_button = page.locator(".special_submit spec_l")

        cart = page.locator("#basket_cena")
        cart.click()

        product_names = page.locator("#basketa > table > tbody").all_inner_texts()

        assert len(product_names) == 2, "V košíku není správný počet produktů."
        assert product_names[0] != product_names[1], "Produkty v košíku jsou stejné, očekávali jsme dva různé produkty."

        browser.close()
