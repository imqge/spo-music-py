from playwright.sync_api import Playwright, sync_playwright, expect
from playwright_recaptcha import recaptchav3,recaptchav2
import random,time,string,re

def MakeNewAccount(email,password,name,birthdate):
    def run(playwright: Playwright) -> None:
        browser = playwright.firefox.launch(headless=False)
        context = browser.new_context()
        page = browser.new_page()
        with recaptchav3.SyncSolver(page) as solver:
            page.goto("https://www.spotify.com/kr-ko/signup")
            page.get_by_placeholder("name@domain.com").click()
            page.get_by_placeholder("name@domain.com").fill(email)
            solver.solve_recaptcha()
            page.wait_for_timeout(500)
            page.get_by_test_id("submit").click()
        page.get_by_label("Use tab to navigate to the").click()
        page.get_by_label("Use tab to navigate to the").fill(password)
        page.wait_for_timeout(500)
        page.get_by_test_id("submit").click()
        page.get_by_label("Name").click()
        page.get_by_label("Name").fill(name)
        year = str(birthdate[:4])
        month = str(birthdate[4:6])
        print(month)
        month_dict = {
            "01": "January", "02": "February", "03": "March", "04": "April",
            "05": "May", "06": "June", "07": "July", "08": "August",
            "09": "September", "10": "October", "11": "November", "12": "December"
        }
        month = month_dict[month]
        print(month)
        day = birthdate[6:8]
        print(day)
        page.get_by_test_id("birthDateYear").click()
        page.get_by_test_id("birthDateYear").fill(year) 
        page.get_by_test_id("birthDateMonth").select_option(month)
        page.get_by_test_id("birthDateDay").click()
        page.get_by_test_id("birthDateDay").fill(day)
        page.locator("label").filter(has_text=re.compile(r"^Man$")).locator("span").first.click()
        page.get_by_test_id("submit").click()
        page.locator("label").filter(has_text="Collection and use of").locator("span").first.click()
        page.locator("label").filter(has_text="Spotify terms and conditions").locator("span").first.click()
        page.get_by_test_id("submit").click()
        page.wait_for_timeout(5000)
        if page.url != "https://www.spotify.com/kr-ko/download/windows/":
            with recaptchav2.SyncSolver(page) as solver:
                token = solver.solve_recaptcha(wait=True)
                page.get_by_role("button", name="continue").click()
        return True
    with sync_playwright() as playwright:
        run(playwright)
