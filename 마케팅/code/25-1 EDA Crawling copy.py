# pip install selenium==4.17.2

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from tqdm import tqdm
import pandas as pd

company_list = ["CJ ENM", "카카오엔터"]

for company in company_list:
    link = f"https://search.naver.com/search.naver?where=news&query={company}&sm=tab_opt&sort=0&photo=3&field=0&pd=5&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3A1y&is_sug_officeid=0&office_category=0&service_area=0"

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(10)

    browser.get(link)
    browser.maximize_window()

    max_scrolls = 50
    current_scroll = 0
    last_height = browser.execute_script("return document.body.scrollHeight")

    while current_scroll < max_scrolls:

        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        new_height = browser.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            print("더 이상 스크롤할 내용이 없습니다.")
            break

        last_height = new_height
        current_scroll += 1

    news_df = []

    main_window = browser.current_window_handle
    elements = browser.find_elements(By.CSS_SELECTOR, "a.info")
    elements = [element for element in elements if element.text == "네이버뉴스"]

    print(f"찾은 네이버뉴스 링크 개수: {len(elements)}")

    for element in tqdm(elements, desc="뉴스 처리 중"):
        browser.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)

        try:
            browser.execute_script("arguments[0].click();", element)
            all_windows = browser.window_handles
            browser.switch_to.window(all_windows[-1])

            if "entertain" in browser.current_url:
                news_date = browser.find_element(By.CSS_SELECTOR, "em.date").text
                news_title = browser.find_element(
                    By.CSS_SELECTOR, "h2.NewsEndMain_article_title__kqEzS"
                ).text
                news_body = browser.find_element(
                    By.CSS_SELECTOR, "div._article_content"
                ).text
            if "sports" in browser.current_url:
                news_date = browser.find_element(
                    By.CSS_SELECTOR, "NewsEndMain_date__xjtsQ"
                ).text
                news_title = browser.find_element(
                    By.CSS_SELECTOR, "h2.NewsEndMain_article_title__kqEzS"
                ).text
                news_body = browser.find_element(
                    By.CSS_SELECTOR, "div._article_content"
                ).text
            else:
                news_date = browser.find_element(
                    By.CSS_SELECTOR, "span.media_end_head_info_datestamp_time"
                ).get_attribute("data-date-time")
                news_title = browser.find_element(By.CSS_SELECTOR, "#title_area").text
                news_body = browser.find_element(By.CSS_SELECTOR, "#dic_area").text

            news_df.append({"제목": news_title, "일시": news_date, "본문": news_body})

            browser.close()
            browser.switch_to.window(main_window)

        except Exception as e:
            print(f"요소 클릭 또는 데이터 수집 중 오류 발생: {e}")

    news_df = pd.DataFrame(news_df)
    news_df.to_csv(f"C:/{company}_뉴스.csv", index=False, encoding="utf-8-sig")
    print(f"{company} 뉴스 데이터가 성공적으로 저장되었습니다.")
