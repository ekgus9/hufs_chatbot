from flask import Flask, jsonify
import sys
import requests
import re
from bs4 import BeautifulSoup
from menu import menu_
from notice import notice_5
from real_test import sss
from weather import todayWeather, nextWeather

from selenium import webdriver
import datetime

application = Flask(__name__)

@application.route("/schedule",methods=['POST'])
def schedule():
    
    url = 'https://builder.hufs.ac.kr/user/indexSub.action?codyMenuSeq=37069&siteId=hufs&menuType=T&uId=4&sortChar=AAA&menuFrame=&linkUrl=04_0101.html&mainFrame=right'
    response = requests.get(url)
    
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.select_one('#hu_cont_mid > div > div > div:nth-child(7) > div.sch02_box.mb10 > table')
        latter = title.get_text()
        text = re.compile('\w.+\w')
        latter = text.findall(latter)
        
        output = '이번 달 학사일정입니다!\n\n'
        
        for l in range(len(latter)):
            if l % 2 == 0: output = output + latter[l]
            else: output = output + ' ' + latter[l] + '\n'
                
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                            "title": "",
                            "description": output,
                            "thumbnail": {
                                "imageUrl": ""
                            },
                            "buttons": [
                                {
                                    "action": "webLink",
                                    "label": "전체 일정보기",
                                    "webLinkUrl": url
                                }
                            ]
                        }
                    }
                ]
            }
        }
        
        return jsonify(res)
    
@application.route("/ss",methods=['POST'])
def ss():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome('/home/ubuntu/Downloads/chromedriver',options=options)
    
    driver.implicitly_wait(3)
    driver.get('https://wis.hufs.ac.kr/jsp/HUFS/cafeteria/frame_view.jsp')
    driver.switch_to.frame('weekiframe') # menuiframe
    date = datetime.datetime.today().weekday() # 월0123456
    
    spot1 = 4
    
    spot_xpath = '//*[@id="form1"]/table/tbody/tr[{}]'.format(spot1)
    driver.find_element(spot_xpath,by=By.XPATH, value=xpath).click() # 식당 선택
    
    driver.switch_to.parent_frame() # 다시 부모 프레임으로 전환
    driver.switch_to.frame('menuiframe')
    
    req = driver.page_source
    soup=BeautifulSoup(req, 'html.parser')
    title = soup.select_one('body > form > table > tbody')
    text = ''
    
    for spot2 in range(1,6):

        text += '- ' + soup.select_one('tr:nth-child({}) > td.headerStyle'.format(1+spot2)).text+ '\n'

        if date == 6 and spot1 != 'do': text += "등록된 메뉴가\n없습니다.\n"
        else:
            spot2_xpath = '/html/body/form/table/tbody/tr[{}]/td[{}]/table'.format(1+spot2,2+date)
            text += soup.select_one('tr:nth-child({}) > td:nth-child({})'.format(1+spot2,2+date)).text + '\n'

    res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": text
                }
            }
        ]
    }
}
    return jsonify(res)
    
@application.route("/inmunmenu",methods=['POST'])
def inmunmenu():
    res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": menu_('inmun',5)
                }
            }
        ]
    }
}
    return jsonify(res)

@application.route("/skymenu",methods=['POST'])
def skymenu():
    res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": menu_('sky',1)
                }
            }
        ]
    }
}
    return jsonify(res)

@application.route("/promenu",methods=['POST'])
def promenu():
    res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": menu_('pro',2)
                }
            }
        ]
    }
}
    return jsonify(res)

@application.route("/hugomenu",methods=['POST'])
def hugomenu():
    res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": menu_('hugo',1)
                }
            }
        ]
    }
}
    return jsonify(res)

@application.route("/domenu",methods=['POST'])
def domenu():
    res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": menu_('do',4)
                }
            }
        ]
    }
}
    return jsonify(res)

@application.route("/umenu",methods=['POST'])
def umenu():
    res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": menu_('u',1)
                }
            }
        ]
    }
}
    return jsonify(res)

@application.route("/humenu",methods=['POST'])
def humenu():
    res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": menu_('hu',1)
                }
            }
        ]
    }
}
    return jsonify(res)

@application.route("/unimenu",methods=['POST'])
def unimenu():
    res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": menu_('uni',1)
                }
            }
        ]
    }
}
    return jsonify(res)

@application.route("/notice",methods=['POST'])
def notice():
    return notice_5()

@application.route("/todayweather",methods=['POST'])
def todayweather():
    
    res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": todayWeather('s')
                }
            }
        ]
    }
}
    return jsonify(res)

@application.route("/todayMweather",methods=['POST'])
def todayMweather():
    
    res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": todayWeather('m')
                }
            }
        ]
    }
}
    return jsonify(res)

@application.route("/nextweather",methods=['POST'])
def nextweather():
    
    res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": nextWeather('s')
                }
            }
        ]
    }
}
    return jsonify(res)

@application.route("/nextMweather",methods=['POST'])
def nextMweather():
    
    res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": nextWeather('m')
                }
            }
        ]
    }
}
    return jsonify(res)
    

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, threaded=True)
