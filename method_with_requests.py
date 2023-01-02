from twocaptcha import TwoCaptcha
import requests
import re
import os
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from config import API_KEY_TWO_CAPTCHA


class CaptchaSolver:
    API_KEY = API_KEY_TWO_CAPTCHA
    solver = TwoCaptcha(apiKey=API_KEY, pollingInterval=3)
    solver.default_timeout = 60

    @staticmethod
    def solve_recaptcha_v3_and_get_token(sitekey, url, action):
        try:
            result = CaptchaSolver.solver.recaptcha(sitekey=sitekey, url=url, action=action, version="v3",
                                                    min_score=0.3, enterprise=0)
        except Exception as ex:
            print("exception with 2captcha:")
            print(ex)
            return False

        return result['code']


def get_js_hash(form_hash):

    with open("form_hash.js", "w") as form_hash_file:
        form_hash_file.write(f"var form_hash = '{form_hash}';")

    path_to_file_get_hash = os.path.abspath("get_js_hash.html")

    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    driver = webdriver.Chrome(options=option)
    driver.maximize_window()
    time.sleep(1)
    driver.get(path_to_file_get_hash)
    time.sleep(1)
    js_hash = driver.find_element(By.ID, value="hash").text
    driver.close()
    driver.quit()
    return js_hash


def get_form_hash(page):

    form_hash = re.search("formHash: \".+\"", page).group(0)
    form_hash = form_hash.replace('formHash: "', '')
    form_hash = form_hash.replace('"', '')
    return form_hash


def sent_request_to_get_result():

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "referer": "https://dev.amidstyle.com/",
    }

    session = requests.Session()
    response = session.get("https://dev.amidstyle.com/")

    if response.status_code != 200:
        print("response status code != 200")
        return False

    form_hash = get_form_hash(response.text)

    js_hash = get_js_hash(form_hash)

    token = CaptchaSolver.solve_recaptcha_v3_and_get_token(sitekey="6LdtwcsgAAAAAHYuReBjhiIUT5L-s50lgoNDlRVq",
                                                           url="https://dev.amidstyle.com/", action="data")

    if token is False:
        print("problem with token")
        return False

    token = CaptchaSolver.solve_recaptcha_v3_and_get_token(sitekey="6LdtwcsgAAAAAHYuReBjhiIUT5L-s50lgoNDlRVq",
                                                           url="https://dev.amidstyle.com/", action="data")

    link = "https://dev.amidstyle.com/api.php"

    data = {"formHash": form_hash,
            "jsHash": js_hash,
            "googleHash": token}

    print(data)

    response = session.post(url=link, data=data, headers=headers)

    if response.status_code != 200:
        print("response status code != 200")
        return False
    print(response.text)

    if response.json().get('sign') is None:
        return False

    return True


def main():
    for attempt in range(3):
        try:
            if sent_request_to_get_result() is True:
                return
        except Exception as ex:
            print(ex)
    print("Something not right")


if __name__ == '__main__':
    main()



