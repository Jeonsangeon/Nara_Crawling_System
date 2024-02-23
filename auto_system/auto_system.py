import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def webCrawling(work_list, announcement_name, deadline, organization):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get('https://www.g2b.go.kr:8101/ep/tbid/tbidList.do?taskClCds=&bidNm=&searchDtType=1&fromBidDt=2024/01/24&toBidDt=2024/02/23&fromOpenBidDt=&toOpenBidDt=&radOrgan=1&instNm=&area=&regYn=Y&bidSearchType=1&searchType=1')

    driver.find_element(By.XPATH, '//*[@id="resultForm"]/div[4]/div/a/span').click()
    
    for work_value in work_list:
        driver.find_element(By.XPATH, f'//*[@id="taskClCds{work_value}"]').click()

    if announcement_name:
        driver.find_element(By.XPATH, '//*[@id="bidNm"]').click()
        element = driver.find_element(By.XPATH, '//*[@id="bidNm"]')
        element.send_keys(announcement_name)

    driver.find_element(By.XPATH, f'//*[@id="setMonth1_{deadline}"]').click()

    if organization:
        driver.find_element(By.XPATH, '//*[@id="instNm"]').click()
        element = driver.find_element(By.XPATH, '//*[@id="instNm"]')
        element.send_keys(organization)
    
    time.sleep(5)

    driver.find_element(By.XPATH, '//*[@id="buttonwrap"]/div/a[1]/span').click()
    announcement_list = list()
    end_of_data = False
    while(True):
        for row in range(1, 10):
            data = list()
            for col in range(1, 10):
                try:
                    value = driver.find_element(By.XPATH, f'//*[@id="resultForm"]/div[2]/table/tbody/tr[{row}]/td[{col}]').text
                    data.append(value)
                except:
                    end_of_data = True
                    break
            if end_of_data:
                break
            announcement_list.append(data)
        if end_of_data:
            break
        try:
            driver.find_element(By.CLASS_NAME, 'default').click()
        except:
            break
        
    return announcement_list