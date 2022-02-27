from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

#@app.route("/weather")
def todayWeather(where):
    
    seoul_url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%9D%B4%EB%AC%B8%EB%8F%99+%EB%82%A0%EC%94%A8'
    mohyeon_url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%AA%A8%ED%98%84+%EB%82%A0%EC%94%A8'
    
    if where == 's': url = seoul_url
    elif where == 'm' : url = mohyeon_url
    
    response = requests.get(url)
    
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        title = soup.select_one('#main_pack > section.sc_new.cs_weather_new._cs_weather > div._tab_flicking > div.content_wrap > div.open > div:nth-child(1) > div > div.weather_info > div')
        weather_text = title.text.split()
        
        if '구름많음' == weather_text[2] or '흐림' == weather_text[2]: weather_text.append('☁️')
        elif '맑음' == weather_text[2]: weather_text.append('🌞')
        elif '흐리고 가끔 비' == weather_text[2]: weather_text.append('🌦️')
        
        res = '''이문동 오늘 날씨{}\n
현재 온도 {}
{}\n
강수확률 {}
습도 {}
바람 {}
미세먼지 {}
초미세먼지 {}'''.format(weather_text[-1],weather_text[4][2:],weather_text[2],\
            weather_text[10],weather_text[12],weather_text[14],weather_text[16],weather_text[18])
        
    return res

#@app.route("/nextweather")
def nextWeather(where):
    
    seoul_url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%82%B4%EC%9D%BC+%EC%9D%B4%EB%AC%B8%EB%8F%99+%EB%82%A0%EC%94%A8'
    mohyeon_url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%82%B4%EC%9D%BC+%EB%AA%A8%ED%98%84+%EB%82%A0%EC%94%A8'
    
    if where == 's': url = seoul_url
    elif where == 'm' : url = mohyeon_url
    
    response = requests.get(seoul_url)
    
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        title = soup.select_one('#main_pack > section.sc_new.cs_weather_new._cs_weather > div._tab_flicking > div.content_wrap > div.open > div:nth-child(1) > div > div.weather_info.type_tomorrow > div > ul')
        weather_text = title.text.split()
        
        res = '''이문동 내일 날씨\n
-오전-
온도 {}
{}
강수확률 {}
미세먼지 {}
초미세먼지 {}
\n-오후-
온도 {}
{}
강수확률 {}
미세먼지 {}
초미세먼지 {}\n'''.format(weather_text[3][2:],weather_text[4],weather_text[6],weather_text[8],weather_text[10],\
    weather_text[14][2:],weather_text[15],weather_text[17],weather_text[19],weather_text[21])
        
    return res
