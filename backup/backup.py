import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def fetch_haneulwiki_pages():
    # 크롬 브라우저를 헤드리스 모드로 실행
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://haneul.wiki")

    # 검색 창을 찾아 "하늘위키:" 입력 후 엔터
    search_box = driver.find_element(By.ID, "searchInput")
    search_box.send_keys("하늘위키:")
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # 페이지가 로드될 시간을 줌

    # 결과에서 문서의 제목과 RAW 내용을 가져옴
    pages = []
    links = driver.find_elements(By.XPATH, "//div[@class='search-result']//a")
    for link in links:
        title = link.text
        link.click()
        time.sleep(1)  # 문서 페이지가 로드될 시간을 줌
        raw_content = driver.find_element(By.XPATH, "//pre").text
        pages.append({"title": title, "content": raw_content})
        driver.back()
        time.sleep(1)  # 검색 결과 페이지로 돌아갈 시간을 줌

    driver.quit()
    return pages

def store_in_db(pages):
    import sqlite3
    conn = sqlite3.connect('haneul_data.db')
    cursor = conn.cursor()

    for page in pages:
        cursor.execute('''
            INSERT INTO data (title, data) VALUES (?, ?)
        ''', (page['title'], page['content']))

    conn.commit()
    conn.close()

def job():
    from datetime import datetime
    print(f"Job started at {datetime.now()}")
    pages = fetch_haneulwiki_pages()
    store_in_db(pages)
    print(f"Job finished at {datetime.now()}")

# 매일 특정 시간에 작업을 예약합니다 (예: 자정 00:00)
import schedule
schedule.every().day.at("00:00").do(job)

# 스케줄러를 실행합니다
while True:
    schedule.run_pending()
    time.sleep(1)
