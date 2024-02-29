import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def notice_search_crawling(work_list, announcement_name, deadline, organization):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    # 나라장터 접속
    driver.get('https://www.g2b.go.kr:8101/ep/tbid/tbidList.do?taskClCds=&bidNm=&searchDtType=1&fromBidDt=2024/01/24&toBidDt=2024/02/23&fromOpenBidDt=&toOpenBidDt=&radOrgan=1&instNm=&area=&regYn=Y&bidSearchType=1&searchType=1')
    # 검색화면으로 이동
    driver.find_element(By.XPATH, '//*[@id="resultForm"]/div[4]/div/a/span').click()
    # (설정)업무 
    for work_value in work_list:
        driver.find_element(By.XPATH, f'//*[@id="taskClCds{work_value}"]').click()
    # (설정)공고명
    if announcement_name:
        driver.find_element(By.XPATH, '//*[@id="bidNm"]').click()
        element = driver.find_element(By.XPATH, '//*[@id="bidNm"]')
        element.send_keys(announcement_name)
    # (설정)공고/개찰일
    driver.find_element(By.XPATH, f'//*[@id="setMonth1_{deadline}"]').click()
    # (설정)기관명
    if organization:
        driver.find_element(By.XPATH, '//*[@id="instNm"]').click()
        element = driver.find_element(By.XPATH, '//*[@id="instNm"]')
        element.send_keys(organization)
    # 검색
    driver.find_element(By.XPATH, '//*[@id="buttonwrap"]/div/a[1]/span').click()
    announcement_list = list()  # Excel에 작성할 데이터
    while(True):
        for row in range(1, 11):
            data = ["", "", "" , "", "", "" , "" , "" , "" , "" , "", "", "", "", "", "", "", ""]
            try:
                data[0] = driver.find_element(By.XPATH, f'//*[@id="resultForm"]/div[2]/table/tbody/tr[{row}]/td[1]/div').text   #업무
            except:
                break
            data[1] = driver.find_element(By.XPATH, f'//*[@id="resultForm"]/div[2]/table/tbody/tr[{row}]/td[3]/div').text   #분류
            data[2] = driver.find_element(By.XPATH, f'//*[@id="resultForm"]/div[2]/table/tbody/tr[{row}]/td[4]/div').text   #공고명
            data[3] = driver.find_element(By.XPATH, f'//*[@id="resultForm"]/div[2]/table/tbody/tr[{row}]/td[5]/div').text   #공고기관
            data[4] = driver.find_element(By.XPATH, f'//*[@id="resultForm"]/div[2]/table/tbody/tr[{row}]/td[6]/div').text
            # 공동수급
            try:
                data[5] = driver.find_element(By.XPATH, f'//*[@id="resultForm"]/div[2]/table/tbody/tr[{row}]/td[9]/div/button').get_attribute('title') 
            except:
                data[5] = driver.find_element(By.XPATH, f'//*[@id="resultForm"]/div[2]/table/tbody/tr[{row}]/td[9]/div').text
            data[17] = driver.find_element(By.XPATH, f'//*[@id="resultForm"]/div[2]/table/tbody/tr[{row}]/td[4]/div/a').get_attribute('href')   #URL
            # 공고명 접속
            driver.find_element(By.XPATH, f'//*[@id="resultForm"]/div[2]/table/tbody/tr[{row}]/td[4]/div/a').click()
            sections = driver.find_elements(By.CLASS_NAME, "section")
            write_budget = False
            for section in sections:
                section_text = section.text.split("\n")
                # 입찰집행 및 진행 정보(입찰개시, 입찰마감, 개찰(입찰)일시, 참가자등록, 공동수급협정서)
                if any(keyword in section_text for keyword in ["입찰개시일시", "입찰서접수 개시일시", "입찰마감일시", "입찰서접수 마감일시", "개찰(입찰)일시", "개찰일시", "입찰참가자격등록", "공동수급협정서"]):
                    p = re.compile("\\d{4}/(0[1-9]|1[0-2])/(0[1-9]|[1-2][0-9]|3[0-1]) (0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])")
                    for index in range(len(section_text)):
                        try:
                            if section_text[index] == "입찰개시일시" or section_text[index] == "입찰서접수 개시일시":
                                if p.match(section_text[index+1]):
                                    data[6] = section_text[index+1]
                            elif section_text[index] == "입찰마감일시" or section_text[index] == "입찰서접수 마감일시":
                                if p.match(section_text[index+1]):
                                    data[7] = section_text[index+1]
                            elif section_text[index] == "개찰(입찰)일시" or section_text[index] == "개찰일시":
                                if p.match(section_text[index+1]):
                                    data[8] = section_text[index+1]
                            elif section_text[index] == "입찰참가자격등록":
                                if p.match(section_text[index+2]):
                                    data[9] = section_text[index+2]
                            elif section_text[index] == "공동수급협정서" and section_text[index+1] == "마감일시":
                                if "마감" in section_text[index+2]:
                                    data[10] = section_text[index+2]
                                break
                        except:
                            pass
                # 예정가격 결정 및 입찰금액 정보(사업금액, 추정금액, 추정가격, 부가가치세, 배정예산) - section
                elif any(keyword in section_text for keyword in ["사업금액", "추정금액", "추정가격", "부가가치세", "배정예산"]):
                    for index in range(len(section_text)):
                        try:
                            if section_text[index] == "사업금액":
                                if section_text[index+2][0] == '￦' or (ord(section_text[index+2][0]) > ord('0') and ord(section_text[index+2][0]) <= ord('9')):
                                    data[11] = section_text[index+2]
                            elif section_text[index] == "추정금액":
                                if section_text[index+1][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                    data[12] = section_text[index+1]
                            elif section_text[index] == "추정가격":
                                if section_text[index+1] == "(부가가치세 불포함)":
                                    if section_text[index+2][0] == '￦' or (ord(section_text[index+2][0]) > ord('0') and ord(section_text[index+2][0]) <= ord('9')):
                                        data[13] = section_text[index+2]
                                else:
                                    if section_text[index+1][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                        data[13] = section_text[index+1]
                            elif section_text[index] == "부가가치세":
                                if section_text[index+1][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                    data[14] = section_text[index+1]
                            elif section_text[index] == "배정예산":
                                if section_text[index+1][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                    data[15] = section_text[index+1]
                        except:
                            pass
                    write_budget = True
                # 투찰 제한(참가가능지역)
                elif "참가가능지역" in section_text:
                    data[16] = section_text[section_text.index("참가가능지역")+1]

            # 예정가격 결정 및 입찰금액 정보(사업금액, 추정금액, 추정가격, 부가가치세, 배정예산) - detail
            if not write_budget:
                try:
                    section_text = driver.find_element(By.CLASS_NAME, "detail").text.split("\n")
                    for index in range(len(section_text)):
                        try:
                            if section_text[index] == "사업금액":
                                if section_text[index+2][0] == '￦' or (ord(section_text[index+2][0]) > ord('0') and ord(section_text[index+2][0]) <= ord('9')):
                                    data[11] = section_text[index+2]
                            elif section_text[index] == "추정금액":
                                if section_text[index+1][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                    data[12] = section_text[index+1]
                            elif section_text[index] == "추정가격":
                                if section_text[index+1] == "(부가가치세 불포함)":
                                    if section_text[index+2][0] == '￦' or (ord(section_text[index+2][0]) > ord('0') and ord(section_text[index+2][0]) <= ord('9')):
                                        data[13] = section_text[index+2]
                                else:
                                    if section_text[index+1][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                        data[13] = section_text[index+1]
                            elif section_text[index] == "부가가치세":
                                if section_text[index+1][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                    data[14] = section_text[index+1]
                            elif section_text[index] == "배정예산":
                                if section_text[index+1][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                    data[15] = section_text[index+1]
                        except:
                            pass
                except:
                    pass
            # print('\033[31m' + f"[ERROR] \"{data[2]}\" 공고의 형식이 올바르지 않습니다" + '\033[0m')
            announcement_list.append(data)
            driver.back()
        try:
            driver.find_element(By.CLASS_NAME, 'default').click()
        except:
            break
        
    return announcement_list

def pre_standard_crawling(agency_option, work_option, business_name):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    # 검색목록 접속
    driver.get('https://www.g2b.go.kr:8081/ep/preparation/prestd/preStdSrch.do?taskClCd=5')
    # 기관별검색 - 공고기관 설정
    if agency_option[0] == 1:
        driver.find_element(By.XPATH, '//*[@id="instCl1"]').click()
    # 기관별검색 - 검색명 설정
    if agency_option[1]:
        driver.find_element(By.XPATH, '//*[@id="instNm"]').click()
        element = driver.find_element(By.XPATH, '//*[@id="instNm"]')
        element.send_keys(agency_option[1])
    # 업무 설정
    for work_value in work_option:
        # 용역 기본설정
        if work_value != 5:
            driver.find_element(By.XPATH, f'//*[@id="taskClCds{work_value}"]"]').click()
    # 품명(사업명) 설정
    if business_name:
        driver.find_element(By.XPATH, '//*[@id="prodNm"]').click()
        element = driver.find_element(By.XPATH, '//*[@id="prodNm"]')
        element.send_keys(business_name)
    # 출력목록수 설정
    driver.find_element(By.XPATH, '//*[@id="recordCountPerPage"]').click()
    driver.find_element(By.XPATH, '//*[@id="recordCountPerPage"]/option[5]').click()
    # 검색
    driver.find_element(By.XPATH, '//*[@id="frmSearch1"]/div[3]/div/a[1]/span').click()
    input_data = list()
    # 크롤링
    init_chapter = True
    page_num = 1
    while True:
        try:
            for row in range(1, 101):
                data = ["", "", "", "", "", "", ""]
                driver.find_element(By.XPATH, f'//*[@id="container"]/div/table/tbody/tr[{row}]/td[4]/div/a').click()
                time.sleep(0.1)
                data_text = driver.find_element(By.CLASS_NAME, 'section').text.split('\n')
                # "품명(사업명)", "사업명", "품명"으로 표시
                if "품명(사업명)" in data_text:
                    data[0] = data_text[data_text.index("품명(사업명)")+1]
                elif "사업명" in data_text:
                    data[0] = data_text[data_text.index("사업명")+1]
                elif "품명" in data_text:
                    data[0] = data_text[data_text.index("품명")+1]
                # 배정예산액
                if "배정예산액" in data_text:
                    data[1] = data_text[data_text.index("배정예산액")+1]
                # "공개일시" 또는 "나라장터 수신일시"로 표시
                if "공개일시" in data_text:
                    data[2] = data_text[data_text.index("공개일시")+1]
                    if data_text[data_text.index("공개일시")+2] != "의견등록마감일시":
                        data[2] = data[2] + " " + data_text[data_text.index("공개일시")+2]
                elif "나라장터 수신일시" in data_text:
                    data[2] = data_text[data_text.index("나라장터 수신일시")+1]
                    if data_text[data_text.index("나라장터 수신일시")+2] != "의견등록마감일시":
                        data[2] = data[2] + " " + data_text[data_text.index("나라장터 수신일시")+2]
                # 의견등록마감일시
                if "의견등록마감일시" in data_text:
                    data[3] = data_text[data_text.index("의견등록마감일시")+1]
                # 공고기관
                if "공고기관" in data_text:
                    data[4] = data_text[data_text.index("공고기관")+1]
                    if data_text[data_text.index("공고기관")+2] != "수요기관":
                        data[4] = data[4] + " " + data_text[data_text.index("공고기관")+2]
                # 수요기관
                if "수요기관" in data_text:
                    data[5] = data_text[data_text.index("수요기관")+1]
                data[6] = driver.current_url
                input_data.append(data)
                driver.back()
            # 1 ~ 10 page
            page_num += 1
            if init_chapter:
                if page_num == 2:
                    driver.find_element(By.XPATH, f'//*[@id="pagination"]/a[{page_num-1}]').click()
                elif page_num == 11:
                    driver.find_element(By.CLASS_NAME, 'next').click()
                    init_chapter = False
                else:
                    driver.find_element(By.XPATH, f'//*[@id="pagination"]/a[{page_num}]').click()
            # 11 ~ page
            else:
                if page_num % 10 == 1:
                    driver.find_element(By.CLASS_NAME, 'next').click()
                else:
                    if page_num % 10 == 0:
                        driver.find_element(By.XPATH, f'//*[@id="pagination"]/a[11]').click()
                    else:
                        driver.find_element(By.XPATH, f'//*[@id="pagination"]/a[{(page_num%10)+1}]').click()
        except:
            break

    return input_data