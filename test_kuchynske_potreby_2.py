import pytest
from playwright.sync_api import sync_playwright


valid_username = "stepanka.kuc@seznam.cz"
valid_password = "engeto"

@pytest.fixture(scope="module", params=["chromium", "firefox", "webkit"])
def setup_browser(request):
    browser_type = request.param
    with sync_playwright() as p:
        browser = getattr(p, browser_type).launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()

@pytest.mark.parametrize("username, password, expected_message",
    [
        ("stepanka.kuc@seznam.cz", "engeto", ""), #všechno správně
        ("c@seznam.cz", "geto", "Zadaná e-mailová adresa není zaregistrována nebo není aktivována!"), #všechno špatně
        ("stepanka.kuc@seznam.cz", "geto", "Zadal(a) jste špatně přihlašovací e-mail nebo heslo."), #správné username, špatně password
        ("stepanka.kuc@seznam.cz", "", ""), #správné username, prázdné password
        ("c@seznam.cz", "", ""), #špatně username, prázdné password
        ("", "", ""), #všechno prázdné
    ]
)
def test_login(setup_browser, username, password, expected_message):
    page = setup_browser
    page.goto("https://www.kuchynskepotreby.cz/")

    prihlaseni_button = page.locator("#header > div > div > div > div.col.account > div > a:nth-child(3)")
    prihlaseni_button.click()

    page.fill('input[name="E-mail"]', username)
    page.fill('input[name="Heslo"]', password)
    page.click('button[type="submit"]')

    page.wait_for_selector(f'text={expected_message}')

    assert expected_message in page.inner_text('body')