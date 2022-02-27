from flask import Flask, jsonify
from menu_preprocessing import preprocessing
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
menu = Flask(__name__)

def menu_(spot1,sss):
    path = '/home/ubuntu/Downloads/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(path,options=options)
    
    driver.implicitly_wait(2)
    driver.get('https://wis.hufs.ac.kr/jsp/HUFS/cafeteria/frame_view.jsp')
    driver.switch_to.frame('weekiframe') # menuiframe
    date = datetime.datetime.today().weekday() # 월0123456
    
    if spot1 == 'inmun': spot1 = 4
    elif spot1 == 'pro': spot1 = 5
    elif spot1 == 'sky': spot1 = 6
    elif spot1 == 'uni': spot1 = 7
    elif spot1 == 'hugo': spot1 = 8
    elif spot1 == 'hu': spot1 = 9
    elif spot1 == 'u': spot1 = 10
    elif spot1 == 'do': spot1 = 11
    
    spot_xpath = '//*[@id="form1"]/table/tbody/tr[{}]'.format(spot1)
    driver.find_element_by_xpath(spot_xpath).click() # 식당 선택
    
    driver.switch_to.parent_frame() # 다시 부모 프레임으로 전환
    driver.switch_to.frame('menuiframe')
    
    if driver.find_element_by_xpath('/html/body/form').text == "등록된 메뉴가 없습니다.": return "등록된 메뉴가\n없습니다."
    
    text = ''
    
    for spot2 in range(1,sss+1):

        spot2_xpath = '/html/body/form/table/tbody/tr[{}]/td[1]'.format(1+spot2)
        text += '- ' + driver.find_element_by_xpath(spot2_xpath).text + '\n'

        if date == 6 and spot1 != 'do': text += "등록된 메뉴가\n없습니다.\n"
        else:
            spot2_xpath = '/html/body/form/table/tbody/tr[{}]/td[{}]/table'.format(1+spot2,2+date)
            text += driver.find_element_by_xpath(spot2_xpath).text + '\n'
    driver.quit()
    return preprocessing(text)
