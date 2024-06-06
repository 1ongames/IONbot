from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import Select
from datetime import datetime
import random #selenium 설정 함수

def load_list_from_txt(file_path): 
 try: 
    with open(file_path, 'r') as file: 
        contents = file.readlines() # 개행문자, 공백 제거
        contents = [line.strip() for line in contents]
        return contents 

now = datetime.now()

def block(document_, blocking, rev) : #문서 편집으로 인한 차단 시 차단하는 함수
    if blocking not in blocked :
        driver.get('https://haneul.wiki/aclgroup?group=차단된 사용자')
        option1 = driver.find_element(By.XPATH,'//*[@id="modeSelect"]') #ACLGroup 창의 아이피, 사용자 이름 여부 선택란
        dropdown1 = Select(option1)
        dropdown1.select_by_value("username")
        option2 = driver.find_element(By.XPATH,'//*[@id="usernameInput"]') #ACLGroup 창의 사용자 이름 입력란
        option2.send_keys(blocking)
        option3 = driver.find_element(By.XPATH,'//*[@id="noteInput"]') #ACLGroup 창의 메모 입력란
        option3.send_keys("%s r%d 긴급차단 | 자동 차단 (잘못된 경우 \'하늘위키:차단 소명 게시판\'에 토론 발제 바랍니다. 오작동 시 \'사용자:jeongjo13/긴급 정지\'에 토론 발제 바랍니다.)" % (block_memo(document_), rev))
        option4 = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/div[2]/form[1]/div[3]/select') #ACLGroup 창의 기간 선택란
        dropdown2 = Select(option4)
        dropdown2.select_by_value("0")
        time.sleep(0.05)
        add_block = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form[1]/div[4]/button') #ACLGroup 창의 추가 버튼
        add_block.click()
        blocked.append(blocking) #다른 사용자가 봇 오작동으로 보고 차단 해제했다면 다시 차단하는 것을 방지하기 위해 차단 제외 목록에 추가

def block_thread(thread, blocking, comment_number) : #토론으로 인한 차단 시 차단하는 함수
    if blocking not in blocked :
        driver.get('https://haneul.wiki/aclgroup?group=차단된 사용자')
        option1 = driver.find_element(By.XPATH,'//*[@id="modeSelect"]') #ACLGroup 창의 아이피, 사용자 이름 여부 선택란
        dropdown1 = Select(option1)
        dropdown1.select_by_value("username")
        option2 = driver.find_element(By.XPATH,'//*[@id="usernameInput"]') #ACLGroup 창의 사용자 이름 입력란
        option2.send_keys(blocking)
        option3 = driver.find_element(By.XPATH,'//*[@id="noteInput"]') #ACLGroup 창의 메모 입력란
        option3.send_keys("토론 %s #%d 긴급차단 | 자동 차단 (잘못된 경우 \'하늘위키:차단 소명 게시판\'에 토론 발제 바랍니다. 오작동 시 \'사용자:jeongjo13/긴급 정지\'에 토론 발제 바랍니다.)" % (thread, comment_number))
        option4 = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/div[2]/form[1]/div[3]/select') #ACLGroup 창의 기간 선택란
        dropdown2 = Select(option4)
        dropdown2.select_by_value("0")
        time.sleep(0.05)
        add_block = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form[1]/div[4]/button') #ACLGroup 창의 추가 버튼
        add_block.click()
        blocked.append(blocking) #다른 사용자가 봇 오작동으로 보고 차단 해제했다면 다시 차단하는 것을 방지하기 위해 차단 제외 목록에 추가

def get_doc_text() : #문서 RAW 읽어오는 함수
    doc_text_field = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/textarea')
    doc_text = doc_text_field.text #문서 RAW 란에 있는 내용 읽어오기
    return doc_text #문서 RAW 반환

def block_memo(name) : #차단 사유에 문서명을 문서:~~~, 하늘위키:~~~과 같이 들어갈 것을 지정해줌
    #만약 문서 이름공간에서의 반달이라면
    if "하늘위키:" not in name :
        if "틀:" not in name :
            if "분류:" not in name :
                if "파일:" not in name :
                    if "휴지통:" not in name :
                        if "사용자:" not in name :
                            if "위키관리:" not in name :
                                if "가상위키:" not in name :
                                    name = "문서:" + name #차단 사유의 문서명 앞에 문서:를 붙임
    return(name) #문서명 반환
def revert(doc, rev) : #반달성 편집 되돌리는 함수
    rev = rev - 1
    driver.get(f"https://haneul.wiki/revert/{doc}?rev={rev:d}") #해당 문서의 정상적인 리비전으로 접속
    try :
        time.sleep(0.5)
        revert_reason = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form/input')
        revert_reason.send_keys("반달 복구: 반달을 멈추시고 하늘위키에 정상적으로 기여해 주시기 바랍니다. | 자동 되돌리기 (잘못된 경우 \'하늘위키:문의 게시판\'에 토론 발제 바랍니다. 오작동 시 \'사용자:jeongjo13/긴급 정지\'에 토론 발제 바랍니다.") #편집 요약
        revert_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form/div/button')
        revert_button.click() #되돌리기 클릭
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        print(f"Error in revert function: {e}")


def trash(doc) : #반달성 문서 휴지통화시키는 함수
    if "사용자" not in doc :
        try :
            driver.get('https://haneul.wiki/delete/%s' % doc)
            delete_reason = driver.find_element(By.XPATH,'//*[@id="logInput"]') # 문서 삭제 시 편집 요약
            delete_reason.send_keys("반달 복구: 반달을 멈추시고 하늘위키에 정상적으로 기여해 주시기 바랍니다. | 자동 삭제 (잘못된 경우 \'하늘위키:문의 게시판\'에 토론 발제 바랍니다. 오작동 시 \'사용자:jeongjo13/긴급 정지\'에 토론 발제 바랍니다.)")
            delete_check = driver.find_element(By.XPATH,'//*[@id="agreeCheckbox"]')
            delete_check.click()
            delete_button = driver.find_element(By.XPATH, '//*[@id="submitBtn"]')
            delete_button.click() #문서 삭제 버튼 클릭
            driver.get('https://haneul.wiki/move/%s' % doc)
            move_document = driver.find_element(By.XPATH,'//*[@id="titleInput"]') #문서 이동 시 사용할 휴지통 문서명
            move_document.send_keys('휴지통:%s' % trashname())
            move_document_memo = driver.find_element(By.XPATH,'//*[@id="logInput"]')
            move_document_memo.send_keys("반달 복구: 반달을 멈추시고 하늘위키에 정상적으로 기여해 주시기 바랍니다. | 자동 휴지통화 (잘못된 경우 \'하늘위키:문의 게시판\'에 토론 발제 바랍니다. 오작동 시 \'사용자:jeongjo13/긴급 정지\'에 토론 발제 바랍니다.)")
            move_button = driver.find_element(By.XPATH,'//*[@id="moveForm"]/div[4]/button')
            move_button.click() #문서 이동 버튼 클릭
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
            print(f"Error in trash function: {e}")

def trashname() : #휴지통화할 때 휴지통 문서명 반환해주는 함수
    a = random.randrange(1000000000, 9999999999) #랜덤한 10자리 수 지정 후
    return (a) #반환

def check_thread(thread) : #토론 주소에서 토론 ~~~의 부분만 반환
    thread = thread[27:] #https://haneul.wiki/thread/부분은 자르고 나머지 부분만 남김 (다른 위키에서 사용 시 수정 필요)
    return(thread) #토론 주소 반환

def check_thread_user(thread) :
    driver.get(thread)
    time.sleep(10) #토론 로딩 완료까지 기다림
    try :
        thread_user_text = driver.find_element(By.XPATH, '//*[@id="res-container"]/div[1]/div/div[1]/a') #1번 댓글 작성자 식별
        thread_user = thread_user_text.text
        return(thread_user) #토론 발제자 값 반환
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) :
        print("[오류!] 토론 발제자를 식별하지 못했습니다.")

def close_thread(thread) : #토론 닫기 함수
    driver.get(thread)
    close_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form[1]/button') #토론 상태 변경에서 '변경' 버튼
    close_button.click()
    time.sleep(1)
    new_document = driver.find_element(By.XPATH, '//*[@id="thread-document-form"]/input') #토론 문서 변경에서 토론 문서를 '휴지통:토론 휴지통'으로
    new_document.send_keys(Keys.CONTROL,'a', Keys.BACKSPACE)
    new_document.send_keys('휴지통:토론 휴지통')
    update_thread_document_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form[2]/button')
    update_thread_document_button.click() #토론 문서 변경 버튼 클릭
    time.sleep(1)
    new_topic = driver.find_element(By.XPATH, '//*[@id="thread-topic-form"]/input')#토론 주제 변경 입력란
    new_topic.send_keys(Keys.CONTROL,'a', Keys.BACKSPACE)
    new_topic.send_keys('.') #새 토론 주제 (강제 조치와 같은 걸로 변경하고 싶으면 이걸 수정 바람)
    update_thread_topic_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form[3]/button')
    update_thread_topic_button.click() # 토론 주제 변경 클릭

# 차단하지 않을 사용자(또는 이미 차단한 사용자(중복 차단 방지)) 리스트
blocked = ["Vanilla","jeongjo13","Cordelia","soupcake27"]
# 감지할 반달성 키워드
vandalism = ["license, Copylight 2024 by iongames, CCL BY-NC-SA 2.0 KR"]
# list.txt 파일로부터 데이터 불러오기
 file_path = 'list.txt' 
 file_content = load_list_from_txt(file_path)
if file_content:
    vandalism.extend(file_content) # 기존 리스트에 추가 
    print(vandalism) # vandalism 값이 list.txt가 제대로 적용되었는지 확인
    # print 값의 시작이 '감지할 반달성 키워드' 주석의 코드와 일치할 경우 정상 작동

# Chrome WebDriver 초기화
driver = webdriver.Chrome()

# 크롬 드라이버에 URL 주소 넣고 실행
driver.get('https://haneul.wiki/member/login?redirect=%2Faclgroup')
time.sleep(2.5)  # 페이지가 완전히 로딩되도록 2.5초 동안 기다림

# data.txt 파일에서 정보 읽어오기
try:
    with open("data.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("wiki_username"):
                wiki_username = line.split(":")[1].strip()
            elif line.startswith("wiki_password"):
                wiki_password = line.split(":")[1].strip()

# data.txt 파일이 없는 경우
except FileNotFoundError:
    wiki_username = input("wiki_username: ")
    wiki_password = input("wiki_password: ")

    # 입력 받은 정보를 data.txt 파일에 저장
    with open("data.txt", "w") as file:
        file.write(f"wiki_username: {wiki_username}\n")
        file.write(f"wiki_password: {wiki_password}\n")

# 입력 받은 정보로 진행
print("wiki_username:", wiki_username)
username = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form/div[1]/input')
username.send_keys(wiki_username)
time.sleep(0.5)

print("wiki_password:", wiki_password)
password = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form/div[2]/input')
password.send_keys(wiki_password)
time.sleep(0.5)

auto_login_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form/div[3]/label/input')
auto_login_button.click()
# 로그인 버튼 클릭
login_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form/button')
login_button.click()
time.sleep(1)

document_names = []
while True :
    try :
        # RecentChanges 페이지로 이동
        driver.get('https://haneul.wiki/RecentChanges?logtype=create')
        time.sleep(0.4)

        # 페이지 소스 가져오기
        page_source = driver.page_source

        # BeautifulSoup을 사용하여 페이지 소스를 파싱
        soup = bs(page_source, 'html.parser')

        # 최근 변경된 문서 목록 추출
        links = soup.find_all('a', href=True)

        # 문서명 추출
        for link in links:
            href = link.get('href')
            if href.startswith('/w/') and link.text.strip():
                document_names.append(link.text.strip())
        try :
            document_names.remove("내 사용자 문서")
        except ValueError :
            print("[오류!] 리스트에서 사용자 문서를 제거할 수 없습니다.")
        print(document_names)

        edited_document = []
        edited_user = []

        for index, value in enumerate(document_names):
            if index % 2 == 0:
                edited_document.append(value)
            else:
                edited_user.append(value)

        print(edited_document)
        print(edited_user)

        for i,j in zip(edited_document,edited_user) :
            if any(v in i for v in vandalism):
                block(i, j, 1)
                trash(i)
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        print("[오류!] 최근 변경의 새 문서 탭을 검토할 수 없습니다.")

    # 문서 변경사항 검토
    # RecentChanges 페이지로 이동
    try :
        driver.get('https://haneul.wiki/RecentChanges')
        time.sleep(0.4)

        # 페이지 소스 가져오기
        page_source = driver.page_source

        # BeautifulSoup을 사용하여 페이지 소스를 파싱
        soup = bs(page_source, 'html.parser')

        # 최근 변경된 문서 목록 추출
        links = soup.find_all('a', href=True)

        # 문서명 추출
        document_names.clear()
        for link in links:
            href = link.get('href')
            if href.startswith('/w/') and link.text.strip():
                document_names.append(link.text.strip())
        num = 0
        for i,j in zip(edited_document,edited_user) :
            driver.get('https://haneul.wiki/history/%s' % i)
            time.sleep(0.5)
            try :
                version = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/ul/li[1]/strong[1]')
                lastest_version = version.text  #해당 문서의 최신 리비전
                lastest_version = lastest_version[1:]
                lastest_version = int(lastest_version)
                if lastest_version > 1 :
                    driver.get("https://haneul.wiki/raw/%s?rev=%d" % (i, lastest_version))
                    time.sleep(0.5)
                    lastest_doc = get_doc_text()
                    driver.get("https://haneul.wiki/raw/%s?rev=%d" % (i, lastest_version-1))
                    time.sleep(0.5)
                    prev_doc = get_doc_text()
                    for k in vandalism :
                        if k in lastest_doc :
                            if k not in prev_doc :
                                block(i, j, lastest_version)
                                revert(i, lastest_version)
                                break
                else :
                    driver.get("https://haneul.wiki/raw/%s?rev=%d" % (i, lastest_version))
                    time.sleep(0.5)
                    lastest_doc = get_doc_text()
                    for k in vandalism :
                        if k in lastest_doc :
                            block(i, j, lastest_version)
                            trash(i)
                            break
            except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
                print("error")
            num += 1;
            if num >= 11 :
                num = 0
                break
            time.sleep(0.01)
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        print("[오류!] 최근 변경의 전체 탭을 검토할 수 없습니다.")

    #사용자 토론을 통한 긴급 정지 여부 확인
    try :
        driver.get('https://haneul.wiki/discuss/%EC%82%AC%EC%9A%A9%EC%9E%90%3Ajeongjo13%2F%EA%B8%B4%EA%B8%89%20%EC%A0%95%EC%A7%80')
        try:
            time.sleep(1)
            element = driver.find_element(By.XPATH, '//*[@id="1"]')
            break
        except NoSuchElementException:
            time.sleep(0.01)
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        print("[오류!] 사용자 토론 긴급 정지 여부를 검토할 수 없습니다.")
    #최근 토론에서 반달성 제목을 가진 토론 추출 및 차단
    try :
        driver.get('https://haneul.wiki/RecentDiscuss')
        time.sleep(0.4)

        # 페이지 소스 가져오기
        page_source = driver.page_source

        # BeautifulSoup을 사용하여 페이지 소스를 파싱
        soup = bs(page_source, 'html.parser')

        threads = []
        thread_url = []
        thread_text = []

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('/thread/'):
                full_url = f"https://haneul.wiki{href}"
                text = a_tag.get_text(strip=True)
                thread_url.append(full_url)
                thread_text.append(text)
        print(thread_url)
        print(thread_text)

        for i,j in zip(thread_text,thread_url) :
            for k in vandalism :
                if k in i :
                    block_thread(check_thread(j), check_thread_user(j), 1)
                    close_thread(j)
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        print("[오류!] 최근 토론의 열린 토론 탭을 검토할 수 없습니다.")
