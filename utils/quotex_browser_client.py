from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_payout(pair):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("https://quotex.com/en/trade/")

    # TODO: Add logic to login to Quotex here (if needed)

    # Placeholder payout value (this is where you'd scrape real payout)
    payout = 95
    driver.quit()
    return payout
