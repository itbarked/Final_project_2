import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture()
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, slow_mo=1000)
        yield browser
        browser.close()

#@pytest.fixture()
#def page(browser):
#    page=browser.new_page()
#    yield page
#    page.close()

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
    
    nejlevnejsi_button = page.locator("#li_price")
    nejlevnejsi_button.click()