from flask import Flask, jsonify
import sys
import requests
import re
from bs4 import BeautifulSoup
from menu import menu_
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
    
@application.route("/menu",methods=['POST'])
def menu_result():
    result = {
      "version": "2.0",
      "data": {
        "inmun": menu_('inmun',5),
        "pro": menu_('pro',2),
        "hugo": menu_('hugo',1),
        "do": menu_('do',4)
        }
    }
    return jsonify(result)

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, threaded=True)
