import json
from time import sleep

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from live_code_bench.leetcode.login_users import users


def _leetcode_submissions_api():
    """
    ! Does not work anymore
    """
    # get_solution_by_problem_language(1, "python")
    problem_id = 1
    language = "python"
    runtime = 100

    leetcode_session = ...
    csrf_token = ...

    res = requests.get(
        f"https://leetcode.com/submissions/api/detail/{problem_id}/{language}/{runtime}/",
        cookies={
            "LEETCODE_SESSION": leetcode_session,
            "csrftoken": csrf_token,
        },
    )
    print(res.status_code, res.reason, res.url)
    print(res.json())


class SeleniumLeetCode:
    SLEEP_TIME = 5

    def __init__(
        self,
        username: str,
        password: str,
        geckodriver_location: str | None = None,
    ):
        options = FirefoxOptions()

        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.headless = True
        options.set_preference("devtools.jsonview.enabled", False)

        service = webdriver.firefox.service.Service(geckodriver_location)

        browser = webdriver.Firefox(
            options=options,
            service=service,
        )

        browser.get("https://leetcode.com/accounts/login/")

        # Login
        sleep(self.SLEEP_TIME)
        browser.find_element(By.ID, "id_login").send_keys(username)
        browser.find_element(By.ID, "id_password").send_keys(password)
        browser.find_element(By.ID, "signin_btn").click()
        # browser.execute_script("arguments[0].click();", sign_in_button)
        sleep(self.SLEEP_TIME)

        self.browser = browser

    def submissions_by_problem_lang_runtime(
        self,
        problem_id,
        language,
        runtime,
    ):
        try:
            self.browser.get(
                f"https://leetcode.com/submissions/api/detail/{problem_id}/{language}/{runtime}/",
            )
            sleep(self.SLEEP_TIME)

            # Search for <pre> tag
            pre = self.browser.find_element(By.TAG_NAME, "pre")
            parsed_json = json.loads(pre.text)
            return parsed_json
        except Exception as e:
            print(e)
            return None


if __name__ == "__main__":
    sl = SeleniumLeetCode(
        username="kingh0730",
        password=users["kingh0730"],
        # geckodriver_location="/home/kingh0730/bin/geckodriver",
    )
    result = sl.submissions_by_problem_lang_runtime(1, "python", 100)
    print(result)
