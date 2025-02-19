from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
import re

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://instagram.com")
time.sleep(3)

# 모듈 호출
from selenium.webdriver.common.keys import Keys

# 인스타 로그인
driver.implicitly_wait(10)
login_id = driver.find_element(By.CSS_SELECTOR, 'input[name="username"]')
login_id.send_keys("")  # 아이디
login_pwd = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
login_pwd.send_keys("")  # 비번
driver.implicitly_wait(10)
login_pwd.submit()
time.sleep(1)
login_id.send_keys(Keys.ENTER)

time.sleep(1)

after_doing = driver.find_element(By.CSS_SELECTOR, "button._acan")
after_doing.click()

time.sleep(1)


def insta_searching(word):
    url = "https://www.instagram.com/explore/search/keyword/?q=%23" + word
    return url


def select_first(driver):
    first = driver.find_element(By.CSS_SELECTOR, "div._aagw")
    first.click()
    time.sleep(3)


def get_content(driver):
    try:
        content = driver.find_element(By.CSS_SELECTOR, "div._a9zr").text
        tags = re.findall(r"#[^\s#,\\]+", content)
        time = driver.find_element(By.CSS_SELECTOR, "time.x1p4m5qa").get_attribute(
            "datetime"
        )[:10]
        data = [content, tags, time]

    except Exception as e:
        return None
    return data


def move_next(driver):
    right = driver.find_elements(By.CSS_SELECTOR, "button._abl-")
    right[1].click()
    time.sleep(3)


word = "송파구"
url = insta_searching(word)
driver.get(url)
time.sleep(5)
select_first(driver)  # 첫 게시글 열기

results = []
target = 100
for i in tqdm(range(target), desc="Crawling"):
    time.sleep(1)
    data = get_content(driver)
    if data:
        results.append(data)
        move_next(driver)
    else:
        move_next(driver)

results = pd.DataFrame(results, columns=["content", "tags", "time"])
results.to_csv(f"C:/instagram_{word}.csv", index=False, encoding="utf-8-sig")

driver.close()
