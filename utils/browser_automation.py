from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def start_browser_login(email, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://quotex.com/en/sign-in")

    time.sleep(2)

    # Fill Email
    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys(email)

    # Fill Password
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(password)

    # Click Login
    login_button = driver.find_element(By.XPATH, '//button[contains(@class, "button")]')
    login_button.click()

    time.sleep(5)

    print("✅ Login Attempted, Current URL:", driver.current_url)

    driver.quit()
