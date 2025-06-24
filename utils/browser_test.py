import time
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Automatically download chromedriver matching your Chrome version
chromedriver_autoinstaller.install()

# Setup Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

# Open Quotex Login Page
driver.get("https://quotex.io/en/trade/options")

time.sleep(10)  # ⚠️ Time to manually login → Email, Password enter kar ke login कर लो

# Example: After login, get page title to confirm
print("✅ Current Page Title:", driver.title)

# Example → Extract some elements like balance
try:
    balance = driver.find_element(By.CLASS_NAME, "balance__value").text
    print("💰 Balance:", balance)
except Exception as e:
    print("⚠️ Balance Not Found:", e)

# Wait or perform tasks
time.sleep(20)

driver.quit()
