from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

def notice_5():
    
    url = 'https://www.hufs.ac.kr/user/indexSub.action?codyMenuSeq=37079&siteId=hufs&menuType=T&uId=4&sortChar=AB&linkUrl=04_0201.html&mainFrame=right'
    response = requests.get(url)
    
    # driver = webdriver.Chrome("C:/Users/user/Downloads/chromedriver_win32/chromedriver.exe")

    # driver.get(url)
    # driver.implicitly_wait(3)

    #driver.find_element_by_xpath('//*[@id="board-container"]/div[2]/form[1]/table/tbody')
    # driver.switch_to.frame("homepage_frame")
    
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        title = soup.select_one('#board-container > div.list > form:nth-child(2) > table > tbody')
        title = title.select('tr > td.title > a')
        tet = [] ; number = []
        for i in range(5):
            com = re.compile('boardSeq=([0-9]+)')
            number.append(com.findall(title[i]['href'])) # 링크만 추출
            tet.append(title[i].text.strip())
        print("https://www.hufs.ac.kr/user/indexSub.action?codyMenuSeq=37079&siteId=hufs&menuType=T&uId=4&sortChar=AB&linkUrl=04_0201.html&mainFrame=right&dum=dum&boardId=41661&page=1&command=view&boardSeq=" + number[0][0])
        res = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "listCard": {
          "header": {
            "title": "공지사항"
          },
          "items": [
            {
              "title": tet[0],
              "description": "",
              "imageUrl": "",
              "link": {
                "web": "https://www.hufs.ac.kr/user/indexSub.action?codyMenuSeq=37079&siteId=hufs&menuType=T&uId=4&sortChar=AB&linkUrl=04_0201.html&mainFrame=right&dum=dum&boardId=41661&page=1&command=view&boardSeq=" + number[0][0]
              }
            },
            {
              "title": tet[1],
              "description": "",
              "imageUrl": "",
              "link": {
                "web": "https://www.hufs.ac.kr/user/indexSub.action?codyMenuSeq=37079&siteId=hufs&menuType=T&uId=4&sortChar=AB&linkUrl=04_0201.html&mainFrame=right&dum=dum&boardId=41661&page=1&command=view&boardSeq=" + number[1][0]
              }
            },
            {
              "title": tet[2],
              "description": "",
              "imageUrl": "",
              "link": {
                "web": "https://www.hufs.ac.kr/user/indexSub.action?codyMenuSeq=37079&siteId=hufs&menuType=T&uId=4&sortChar=AB&linkUrl=04_0201.html&mainFrame=right&dum=dum&boardId=41661&page=1&command=view&boardSeq=" + number[2][0]
              }
            }
          ],
          "buttons": [
            {
              "label": "공지사항 더보기",
              "action": "webLink",
              "webLinkUrl": url
            }
          ]
        }
      }
    ]
  }
}
        
    return jsonify(res)
