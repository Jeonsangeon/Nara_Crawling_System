import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def webCrawling(work_list, announcement_name, deadline, organization):
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
            data = ["", "", "" , "" , "" , "" , "" , "" , "" , "", "", "", "", "", "", ""]
            try:
                data[0] = driver.find_element(By.XPATH, f'//*[@id="resultForm"]/div[2]/table/tbody/tr[{row}]/td[1]/div').text
            except:
                break
            data[1] = driver.find_element(By.XPATH, f'//*[@id="resultForm"]/div[2]/table/tbody/tr[{row}]/td[3]/div').text
            data[2] = driver.find_element(By.XPATH, f'//*[@id="resultForm"]/div[2]/table/tbody/tr[{row}]/td[4]/div').text
            data[3] = driver.find_element(By.XPATH, f'//*[@id="resultForm"]/div[2]/table/tbody/tr[{row}]/td[5]/div').text
            data[4] = driver.find_element(By.XPATH, f'//*[@id="resultForm"]/div[2]/table/tbody/tr[{row}]/td[9]/div').text
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
                                    data[5] = section_text[index+1]
                            elif section_text[index] == "입찰마감일시" or section_text[index] == "입찰서접수 마감일시":
                                if p.match(section_text[index+1]):
                                    data[6] = section_text[index+1]
                            elif section_text[index] == "개찰(입찰)일시" or section_text[index] == "개찰일시":
                                if p.match(section_text[index+1]):
                                    data[7] = section_text[index+1]
                            elif section_text[index] == "입찰참가자격등록":
                                if p.match(section_text[index+2]):
                                    data[8] = section_text[index+2]
                            elif section_text[index] == "공동수급협정서" and section_text[index+1] == "마감일시":
                                if "마감" in section_text[index+2]:
                                    data[9] = section_text[index+2]
                                break
                        except:
                            pass
                # 예정가격 결정 및 입찰금액 정보(사업금액, 추정금액, 추정가격, 부가가치세, 배정예산) - section
                elif any(keyword in section_text for keyword in ["사업금액", "추정금액", "추정가격", "부가가치세", "배정예산"]):
                    for index in range(len(section_text)):
                        try:
                            if section_text[index] == "사업금액":
                                if section_text[index+1][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                    data[10] = section_text[index+2]
                            elif section_text[index] == "추정금액":
                                if section_text[index+1][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                    data[11] = section_text[index+1]
                            elif section_text[index] == "추정가격":
                                if section_text[index+1] == "(부가가치세 불포함)":
                                    if section_text[index+2][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                        data[12] = section_text[index+2]
                                else:
                                    if section_text[index+1][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                        data[12] = section_text[index+1]
                            elif section_text[index] == "부가가치세":
                                if section_text[index+1][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                    data[13] = section_text[index+1]
                            elif section_text[index] == "배정예산":
                                if section_text[index+1][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                    data[14] = section_text[index+1]
                        except:
                            pass
                    write_budget = True
                # 투찰 제한(참가가능지역)
                elif "참가가능지역" in section_text:
                    data[15] = section_text[section_text.index("참가가능지역")+1]
            # 예정가격 결정 및 입찰금액 정보(사업금액, 추정금액, 추정가격, 부가가치세, 배정예산) - detail
            if not write_budget:
                try:
                    section_text = driver.find_element(By.CLASS_NAME, "detail").text.split("\n")
                    for index in range(len(section_text)):
                        try:
                            if section_text[index] == "사업금액":
                                if section_text[index+1][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                    data[10] = section_text[index+2]
                            elif section_text[index] == "추정금액":
                                if section_text[index+1][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                    data[11] = section_text[index+1]
                            elif section_text[index] == "추정가격":
                                if section_text[index+1] == "(부가가치세 불포함)":
                                    if section_text[index+2][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                        data[12] = section_text[index+2]
                                else:
                                    if section_text[index+1][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                        data[12] = section_text[index+1]
                            elif section_text[index] == "부가가치세":
                                if section_text[index+1][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                    data[13] = section_text[index+1]
                            elif section_text[index] == "배정예산":
                                if section_text[index+1][0] == '￦' or (ord(section_text[index+1][0]) > ord('0') and ord(section_text[index+1][0]) <= ord('9')):
                                    data[14] = section_text[index+1]
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