import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture()
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=1500)
        yield browser
        browser.close()

@pytest.fixture()
def page(browser):
    page=browser.new_page()
    yield page
    page.close()

def test_price_sorting(page):
    url="https://www.kuchynskepotreby.cz/"
    page.goto(url)

    reject_cookies_button = page.locator("#xx-cookies-plugin > div.cp-content-wrap.no-transition > div > p:nth-child(5) > a")
    reject_cookies_button.click() 

    organizace_kuchyne_button = page.locator("#menu > div > ul > li:nth-child(7) > a")
    organizace_kuchyne_button.click()
    
    bloky_na_noze_button = page.locator("#content > ul > li:nth-child(4) > a > span")
    bloky_na_noze_button.click()
    
    znacka_orion_checkbox = page.locator("#maklab57")
    znacka_orion_checkbox.check()
    
    page.wait_for_load_state("networkidle", timeout=30000)

    nejlevnejsi_button = page.locator("#li_price")
    page.wait_for_selector("#li_price", state="visible", timeout=10000)
    nejlevnejsi_button.click()

    page.wait_for_load_state("networkidle", timeout=30000)

    products_wrap = page.query_selector(".products-wrap.v2")
    products = products_wrap.query_selector_all(".price")
    prices = []
    
    for product in products:
            price_element = product.query_selector(".price")
            if price_element:
                price_text = price_element.inner_text().replace(" Kč", "").strip()
                try:
                    price = float(price_text.replace(",", "."))
                    prices.append(price)
                except ValueError:
                    pass
    assert prices == sorted(prices), "Produkty nejsou seřazeny podle ceny od nejlevnější po nejdražší."