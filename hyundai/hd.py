import requests
import hashlib
from selenium import webdriver
from bs4 import BeautifulSoup
from binascii import crc32
from random import randint
import time, warnings
import pandas as pd
from datetime import datetime
import cloudscraper

warnings.simplefilter("ignore", UserWarning)

# MongoDB
try:
    import pymongo
except:
    print ("Install pymongo Library : pip3 install pymongo")

#만약 해당 사이트측에서 차단할 경우를 대비해서 tor 이용해야함!
###### Tor Setting ######
proxies = {
    "http": "socks5h://localhost:9050",
    "https": "socks5h://localhost:9050"
}

###### Header Setting ######
headers =   { 
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0", 
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
                'Accept-Encoding':'gzip, deflate', 
                'Accept-Language':'en-US,en;q=0.5',
                'Cache-Control': 'no-cache', 
                'Connection': 'keep-alive', 
                'Pragma':'no-cache',
                'Referer':'http://xfr3txoorcyy7tikjgj5dk3rvo3vsrpyaxnclyohkbfp3h277ap4tiad.onion/'
            }

###### MongoDB Setting ######
host="localhost"
port="27017"
client = pymongo.MongoClient(host, int(port))
db = client["cardata"]

###### Setting ######
BASE_PATH = "/Users/macbookpro/workspace/cardata/hyundai/"
sitename = "HYUNDAI"
EXCUTABLE_PATH = "/Users/macbookpro/workspace/chromedriver"
#p_ipcheck_url = "https://ident.me"


def screencapture(id, link) :
    image_fname = '{}capture/{}_{}.png'.format(BASE_PATH, sitename, id)
    settings = {}
    settings['MAX_RETRIES'] = 3
    # settings['CHROME_PROXY'] = '127.0.0.1:9050'
    settings['CHROME_OPTIONS'] = ["--no-sandbox", "--disable-dev-shm-usage", "--disable-extensions", "--disable-gpu",
        "--disable-setuid-sandbox", "--ignore_ssl", "--dns-prefetch-disable", '--allow-running-insecure-content',
        "--ignore-certificate-errors","--hide-scrollbars",
        # '--proxy-server=socks5://127.0.0.1:9050',
        "--headless"]
    settings['CHROME_EXCUTE']  = "/Users/macbookpro/workspace/chromedriver"
    settings['DO_SAVE_HTML'] = True

    options = webdriver.ChromeOptions()
    for opt in settings['CHROME_OPTIONS']:
        options.add_argument(opt)
    options.add_argument("user-agent={}".format('Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'))

    driver = webdriver.Chrome(EXCUTABLE_PATH, options=options) # executable path
    driver.implicitly_wait(30)
    driver.get(link)
    page_width = driver.execute_script('return document.body.parentNode.scrollWidth') + 350
    page_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(page_width, page_height)

    driver.save_screenshot(image_fname)

    driver.quit()
    return image_fname

def HYUNDAI():
    
    hd_url = "https://www.hyundai.com/kr/ko/event"
    page_url = hd_url
    ##### 자바스크립트 페이지이므로 selenium 이용
    settings = {}
    settings['MAX_RETRIES'] = 3
    settings['CHROME_OPTIONS'] = ["--no-sandbox", "--disable-dev-shm-usage", "--disable-extensions", "--disable-gpu",
        "--disable-setuid-sandbox", "--ignore_ssl", "--dns-prefetch-disable", '--allow-running-insecure-content',
        "--ignore-certificate-errors",
        "--headless"]
    settings['CHROME_EXCUTE']  = "/Users/macbookpro/workspace/chromedriver"
    settings['DO_SAVE_HTML'] = True

    options = webdriver.ChromeOptions()
    for opt in settings['CHROME_OPTIONS']:
        options.add_argument(opt)
    options.add_argument("user-agent={}".format('Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'))

    driver = webdriver.Chrome(EXCUTABLE_PATH, options=options) # executable path
    driver.implicitly_wait(30)

    hd_get = driver.get(page_url)

    hd_content = driver.page_source

    print(" requests complete")
    soup = BeautifulSoup(hd_content, features="html.parser") # from_encoding='cp949'
    hyundai_event = db["hyundai_event"]

    #####content#####

    # html 보기 및 저장
    '''
    presoup = soup.prettify()
    print(presoup)
    f = open('hyundai_event.html', 'w', -1, 'utf-8')
    f.write(presoup)
    f.close()
    print('현대자동차 이벤트 페이지 저장완료!')
    '''
    content = soup.find('div', {'class':'tab_contents'})
    eventlist = content.find('ul', {'class':'image_board'}) #이벤트 리스트

    for event in eventlist.find_all('li'): # 각각 하나하나의 이벤트
        alink = event.find('a')
        link = alink['href']

        text = event.find('div') # text 정보수집
        title = ''
        target = ''
        date = ''
        if(text.find('<p class="title">')!=-1):
            # print(text)
            title = text.find('b').get_text()
        if(text.find('<p class="info">')!=-1):
            target = text.find('span').get_text()
            date = text.find('span', {'class':'num'}).get_text()

        id = crc32(title.encode()) #PK를 만들어주기 위해 title을 crc32로 인코딩함

        print(id)
        print(title)
        print(target)
        print(date)

        # 이미지 파일 경로설정
        image = "{}_{}.png".format(sitename, id)
        
        try:
            hyundai_event.insert_one({"_id":id, "title":title, "target":target, "date":date, "image":image})
            print("@@ DB insert complete")

            try:
                capture_filename = screencapture(id, link)
                print("@@ ScreenCapture complate")
                print("----------------------------------")
            except Exception as e:
                    print(e)
                    print ("ScreenCapture Error")

        except Exception as e:
            print(e)

    return
 
if __name__ == '__main__':
    #print ("My Tor IP :", requests.get(p_ipcheck_url, proxies=proxies, headers=headers).text)
    print("HYUNDAI")
    HYUNDAI()
