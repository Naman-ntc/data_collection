from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging


from live_code_bench.leetcode.login_users import users


def login_main(username, password, retry=3):
    if retry == 0:
        return -1
    print(f"Logging in as {username}... {password}")

    # chrome_options = ChromeOptions()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument(
    #     "--disable-gpu"
    # )  # Optional argument, might be needed for stability
    # chrome_options.add_argument(
    #     "--no-sandbox"
    # )  # Optional argument, might be needed for permissions

    # chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})



    # browser = webdriver.Chrome(options=chrome_options)


    options = FirefoxOptions()
    
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.headless = True

    service = webdriver.firefox.service.Service('/snap/bin/geckodriver') 

    browser = webdriver.Firefox(options=options, service=service)

    browser.get("https://leetcode.com/accounts/login/")

    # Login
    sleep(20)
    browser.find_element(By.ID, "id_login").send_keys(username)
    browser.find_element(By.ID, "id_password").send_keys(password)
    browser.find_element(By.ID, "signin_btn").click()
    # browser.execute_script("arguments[0].click();", sign_in_button)
    sleep(20)



    # wait = WebDriverWait(browser, 10)
    # username_input = wait.until(EC.presence_of_element_located((By.ID, "id_login")))
    # password_input = wait.until(EC.presence_of_element_located((By.ID, "id_password")))
    # signin_button = wait.until(EC.element_to_be_clickable((By.ID, "signin_btn")))

    # username_input.send_keys(username)
    # password_input.send_keys(password)
    # signin_button.click()


    # snapshot
    # browser.save_screenshot("screenshot.png")

    # Get cookies
    cookies = browser.get_cookies()

    # Get LEETCODE_SESSION
    leetcode_session_cookies = [
        cookie for cookie in cookies if cookie["name"] == "LEETCODE_SESSION"
    ]
    if leetcode_session_cookies:
        print("Login success!")
    else:
        # logs = browser.get_log('browser')
        # for log in logs:
        #     print(log)
        print("Retrying!!!")
        return login_main(username, password, retry=retry - 1)
        # print(cookies)
        # import pdb

        # pdb.set_trace()
        # raise Exception("Login failed!")

    browser.quit()
    return leetcode_session_cookies[0]["value"]


def login_by_index(index, update_env=True):
    user_password = list(users.items())[index]
    cookie = login_main(*user_password)
    if cookie == -1:
        return
    if update_env:
        with open(".env", "w") as f:
            f.write(f'LEETCODE_SESSION="{cookie}"')


if __name__ == "__main__":
    login_by_index(7, True)
