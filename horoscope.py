#-*- coding=utf8 -*-
import sys
import urllib.request
from bs4 import BeautifulSoup
import time
import html5lib 

def download(url,headers):
    try:
        request = urllib.request.Request(url,headers=headers)
        html = urllib.request.urlopen(request).read().decode("utf-8")
        # html = urllib.urlopen(url).read()
    except urllib.URLError as e:
        print ("error")
        print (e.code)   #可以打印出来错误代号如404。
        print (e.reason)  #可以捕获异常
        html = None
    return html
def save(html):
    f = open('thefile.txt', 'w')
    f.write(html)
    f.close()
def read_file():
    f = open('thefile.txt', 'r')
    html = f.read()
    f.close()
    return html
def get_html(url):
    User_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    headers = {'User_agent': User_agent}
    html = download(url, headers)
    save(html)
def constellation(k,v):
    url = 'http://www.xzw.com/fortune/'+k+'/1.html'
    get_html(url)
    html = read_file()
    soup = BeautifulSoup(html, "html5lib")
    # print soup.find_all('dl')
    html2 = soup.find('div', class_='c_cont')
    html2 = str(html2)
    # print(html2)
    soup = BeautifulSoup(html2,"html5lib")
    text = v+'明日运势：' + '\n'
    text = text + '整体运势：' + soup.find_all('span')[0].string + '\n'
    text = text + '爱情运势：' + soup.find_all('span')[1].string + '\n'
    text = text + '事业学业：' + soup.find_all('span')[2].string + '\n'
    text = text + '财富运势：' + soup.find_all('span')[3].string + '\n'
    text = text + '健康运势：' + soup.find_all('span')[4].string + '\n'
    return text
    # html = urllib.urlopen(url)
    # print html
if __name__=='__main__':

    horoscopes = {'aries':'白羊座','taurus':'金牛座','gemini':'双子座','cancer':'巨蟹座','leo':'狮子座','virgo':'处女座','libra':'天秤座','scorpio':'天蝎座','sagittarius':'人马座','capricorn':'摩羯座','aquarius':'水瓶座','pisces':'双鱼座'}
    for k,v in horoscopes.items():
        text = constellation(k,v)
        print(text)