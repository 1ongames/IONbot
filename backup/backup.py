pip install requests schedule

import requests
import sqlite3
import schedule
import sqlite3
import schedule
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def fetch_haneulwiki_pages():
    options = Options()
    options.headless = True  # 헤드리스 모드로 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://haneul.wiki")

    # 검색 창을 찾아 "하늘위키:" 입력 후 엔터
    search_box = driver.find_element(By.XPATH, "//input[@type='search']")  # 검색창의 XPATH
    search_box.send_keys("하늘위키:")
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # 페이지가 로드될 시간을 줌

    # 결과에서 문서의 제목과 RAW 내용을 가져옴
    pages = []
    links = driver.find_elements(By.XPATH, "//div[@class='search-result']//a")  # 결과 링크의 XPATH
    for link in links:
        title = link.text
        link.click()
        time.sleep(1)  # 문서 페이지가 로드될 시간을 줌
        raw_content = driver.find_element(By.XPATH, "//pre").text  # RAW 내용의 XPATH
        pages.append({"title": title, "content": raw_content})
        driver.back()
        time.sleep(1)  # 검색 결과 페이지로 돌아갈 시간을 줌

    driver.quit()
    return pages

def store_in_db(pages):
    conn = sqlite3.connect('haneul_data.db')
    cursor = conn.cursor()
    
    for page in pages:
        cursor.execute('''
            INSERT INTO data (title, data) VALUES (?, ?)
        ''', (page['title'], page['content']))
    
    conn.commit()
    conn.close()

def job():
    print(f"Job started at {datetime.now()}")
    pages = fetch_haneulwiki_pages()
    store_in_db(pages)
    print(f"Job finished at {datetime.now()}")

# Schedule the job every day at a specific time, e.g., 00:00 (midnight)
schedule.every().day.at("00:00").do(job)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)

from datetime import datetime

def save_edit_history(title, ip, send, previous_content, new_content):
    conn = sqlite3.connect('haneul_data.db')
    cursor = conn.cursor()

    # 현재 시간을 가져옴
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # IP 주소에 "H:"를 추가
    ip = "H:" + ip

    # 추가된 글자 수 계산
    added_length = len(new_content) - len(previous_content)

    # 해당 문서의 마지막 리비전 번호 가져오기
    cursor.execute('''
        SELECT MAX(id) FROM history WHERE title = ?
    ''', (title,))
    last_revision = cursor.fetchone()[0]
    if last_revision is None:
        last_revision = 0
    else:
        last_revision += 1

    # 첫 번째 리비전의 경우 id를 1로 설정
    if last_revision == 0:
        last_revision = 1

    # history 테이블에 데이터 삽입
    cursor.execute('''
        INSERT INTO history (id, title, date, ip, send, leng) VALUES (?, ?, ?, ?, ?, ?)
    ''', (last_revision, title, now, ip, send, added_length))

    conn.commit()
    conn.close()

# 예시: save_edit_history("문서 제목", "192.168.0.1", "내용을 수정함", "이전 내용", "새로운 내용")
