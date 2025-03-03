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

def test_kuchynske_potreby(page):
    url="https://www.kuchynskepotreby.cz/"
    page.goto(url)

    reject_cookies_button = page.locator("#xx-cookies-plugin > div.cp-content-wrap.no-transition > div > p:nth-child(5) > a") #odkliknu cookies
    reject_cookies_button.click() 

    organizace_kuchyne_button = page.locator("#menu > div > ul > li:nth-child(7) > a") #proklikám se ke stojanům na nože značky Orion srovnané od nejlevnějšího
    organizace_kuchyne_button.click()
    
    bloky_na_noze_button = page.locator("#content > ul > li:nth-child(4) > a > span")
    bloky_na_noze_button.click()
    
    znacka_orion_checkbox = page.locator("#maklab57")
    znacka_orion_checkbox.check()
    
    page.wait_for_selector(".item", state="visible", timeout=10000)

    nejlevnejsi_button = page.locator("#li_price")
    page.wait_for_selector("#li_price", state="visible", timeout=10000)
    nejlevnejsi_button.click()

    page.wait_for_selector(".item", state="visible", timeout=10000)

    #kontrola, že jsou ceny skutečně srovnány od nejnižší po nejvyšší
    prices = page.query_selector_all(".price")
    price_values = []
    
    for price in prices:
        price_text = price.inner_text()
        price_text = price_text.replace(" Kč", "").replace("0\nPřejít k objednávce", "0").strip()
        price_number = float(price_text.replace(",", "."))
        price_values.append(price_number)  
        print(price_values)
        assert price_values == sorted(price_values), "Ceny nejsou seřazeny vzestupně."