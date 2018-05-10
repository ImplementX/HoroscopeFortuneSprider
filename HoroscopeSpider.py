#-*- coding=utf8 -*-
import sys
import urllib.request
from bs4 import BeautifulSoup
import time
import html5lib 
import os
import datetime

horoscopes = {'Aries':'1','Taurus':'2','Gemini':'3','Cancer':'4','Leo':'5','Virgo':'6','Libra':'7','Scorpio':'8','Sagittarius':'9','Capricorn':'10','Aquarius':'11','Pisces':'12'}
types = {'SUN SIGH':'general','LOVE':'love','CAREER':'career','MONEY':'money','HEALTH':'wellness'}
times = { 'Today':'daily-today','Tomorrow':'daily-tomorrow','Thisweek':'weekly','Thismonth':'monthly'}
DATETIME = ""

def download(url,headers):
    try:
        request = urllib.request.Request(url,headers=headers)
        html = urllib.request.urlopen(request).read().decode("utf-8")
        # html = urllib.urlopen(url).read()
    # except urllib.error.HTTPError:
    #     raise
    except urllib.URLError as e:
        print ("error")
        print (e.code)   #可以打印出来错误代号如404。
        print (e.reason)  #可以捕获异常
        html = None
    

    return html
def save(html):
    f = open('thefile.txt', 'w',encoding='utf-8')
    f.write(html)
    f.close()
def read_file():
    f = open('thefile.txt', 'r',encoding='utf-8')
    html = f.read()
    f.close()
    return html
def get_html(url):
    User_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    headers = {'User_agent': User_agent}
    try:
        html = download(url, headers)
    except:
        raise
    save(html)

def url_handler(horoscope,type,time):
    if type =='MONEY' and time != 'Thisweek':
            return ""
    if type == "LOVE" and (time == "Thismonth" or time == "Thisweek"):
        url1 = 'https://www.horoscope.com/us/horoscopes/'+types[type]+'/horoscope-'+types[type]+'-'+times[time]+'-single'+'.aspx?sign='+horoscopes[horoscope]
        url2 = 'https://www.horoscope.com/us/horoscopes/'+types[type]+'/horoscope-'+types[type]+'-'+times[time]+'-couple'+'.aspx?sign='+horoscopes[horoscope]
        return type+ ":\nIf you are single"+': '   +constellation(url1) + "If you are attached:"      +constellation(url2)
    else:
        url = 'https://www.horoscope.com/us/horoscopes/'+types[type]+'/horoscope-'+types[type]+'-'+times[time]+'.aspx?sign='+horoscopes[horoscope]
        return type+': ' + constellation(url)


def constellation(url):
    global DATETIME
    try:
        get_html(url)
    except urllib.error.HTTPError as e:
        return ''
    html = read_file()
    soup = BeautifulSoup(html, "lxml")
    DATETIME = soup.find('b',class_="date").get_text()
    # print soup.find_all('dl')
    html2 = soup.find('div', class_='horoscope-content')
    html2 = str(html2)
    # print(html2)
    soup = BeautifulSoup(html2,"lxml")
    
    text = soup.find('p').get_text()+ '\n'
    
    text = text.replace(DATETIME,"")
    return text
    # html = urllib.urlopen(url)
    # print html 

def today_match():
    html = read_file()
    soup = BeautifulSoup(html,"lxml")
    love = soup.find('a',id="src-horo-matchlove").h4.get_text()
    friendship = soup.find('a',id="src-horo-matchfriend").h4.get_text()
    career = soup.find('a',id="src-horo-matchcareer").h4.get_text()

    text ="\nToday's Matches: \n" + " Love: " + love + "   Friendship: " + friendship + "   Career: " + career +"\n\n"
    return text

def result(horoscope,time):
    text = horoscope + ' ' +time+': \n'
    
    for type in types:
        
        text =text + url_handler(horoscope,type,time)
    if(time == 'Today'):
        text =  today_match() + text 

    # print(friendship)
    return text
def yearly(horoscope):

    
    nowTime=datetime.datetime.now().strftime('%Y');
    # print(nowTime)
    url = 'https://www.horoscope.com/us/horoscopes/yearly/'+nowTime+'-horoscope-'+horoscope.lower() +'.aspx'
    get_html(url)
    html = read_file()
    # print(html)
    soup = BeautifulSoup(html,"lxml")
    text = soup.find('div',id = "personal").p.get_text()
    # print(text)
    return text
if __name__=='__main__':
    path ="/data/tools/nginx/html/horoscope/"
    # path = "horoscope/"
    yearly('Aries')
    # text =result("Aries","Today")
    # text = DATETIME  +" "+ text
    # print(text)
    for horoscope in horoscopes:
        for time in times:
            print(horoscope+" "+time)
            text =result(horoscope,time)
            text = DATETIME  +" "+ text
            print(text)
            if not os.path.exists(path+horoscope.lower()+'/'):
                os.makedirs(path+horoscope.lower()+'/') 
            f = open(path+horoscope.lower()+'/'+ time.lower() + ".txt", 'w',encoding='utf-8')
            f.write(text)
            f.close()
        text = yearly(horoscope)
        if not os.path.exists(path+horoscope.lower()+'/'):
                os.makedirs(path+horoscope.lower()+'/') 
        f = open(path+horoscope.lower()+'/'+ 'thisyear' + ".txt", 'w',encoding='utf-8')
        f.write(text)
        f.close()
    
    
    