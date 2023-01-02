import selenium
from selenium import webdriver
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import json
import traceback


def main(link):

    try:
        for attempt in range(3):
            option = webdriver.ChromeOptions()
            #option.add_argument("--headless")
            driver = uc.Chrome(options=option)
            #driver = webdriver.Chrome(options=option)
            driver.maximize_window()
            time.sleep(2)
            driver.get(link)
            time.sleep(5)
            data = driver.find_element(By.ID, value="data").text
            data = json.loads(data)
            if data.get('sign') is not None:
                print("response:")
                print(data)
                print("sign:")
                print(data['sign'])
                driver.close()
                driver.quit()
                return data
            else:
                print("some error, response:")
                print(data)
            driver.close()
            driver.quit()
        return False

    except Exception:
        print("Opps.. Some exception")
        traceback.print_exc()


if __name__ == '__main__':
    main(link="https://dev.amidstyle.com/")