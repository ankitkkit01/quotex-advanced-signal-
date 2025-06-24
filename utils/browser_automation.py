from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def start_browser_login(email, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get("https://quotex.com/en/sign-in")
        time.sleep(2)

        # Fill Email
        email_input = driver.find_element(By.NAME, "email")
        email_input.clear()
        email_input.send_keys(email)

        # Fill Password
        password_input = driver.find_element(By.NAME, "password")
        password_input.clear()
        password_input.send_keys(password)

        # Click Login
        login_button = driver.find_element(By.XPATH, '//button[contains(@class, "button")]')
        login_button.click()

        time.sleep(5)

        print("✅ Login Attempted, Current URL:", driver.current_url)

    except Exception as e:
        print(f"❌ Error during login: {e}")

    finally:
        driver.quit()
