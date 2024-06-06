pip install requests schedule

import requests
import sqlite3
import schedule
import time
from datetime import datetime

def fetch_haneulwiki_pages():
    url = "https://haneul.wiki/api.php?action=query&list=allpages&apnamespace=0&format=json"
    response = requests.get(url)
    data = response.json()
    pages = data['query']['allpages']
    return [{"title": page['title'], "content": fetch_page_content(page['title'])} for page in pages if "하늘위키" in page['title']]

def fetch_page_content(title):
    # 이 함수는 각 문서의 내용을 가져오는 로직을 포함해야 합니다.
    # 여기서는 예시로 하드코딩된 데이터를 사용합니다.
    # 실제로는 API 호출이나 웹 스크래핑 등을 통해 내용을 가져와야 합니다.
    return f"내용: {title}"

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
