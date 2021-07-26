import requests
import hashlib
from selenium import webdriver
from bs4 import BeautifulSoup
from binascii import crc32
from random import randint
import time, warnings
import pandas as pd
from datetime import datetime


warnings.simplefilter("ignore", UserWarning)

# MongoDB
try:
    import pymongo
except:
    print ("Install pymongo Library : pip3 install pymongo")

###### Setting ######
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
BASE_PATH = "/Users/macbookpro/workspace/cardata/kia/"
sitename = "KIA"
EXCUTABLE_PATH = "/Users/macbookpro/workspace/chromedriver"
#p_ipcheck_url = "https://ident.me"


def screencapture(id, link) :

    image_fname = '{}capture/{}_{}.png'.format(BASE_PATH, sitename, id)
    settings = {}
    settings['MAX_RETRIES'] = 3
    # settings['CHROME_PROXY'] = '127.0.0.1:9050'
    settings['CHROME_OPTIONS'] = ["--no-sandbox", "--disable-dev-shm-usage", "--disable-extensions", "--disable-gpu",
        "--disable-setuid-sandbox", "--ignore_ssl", "--dns-prefetch-disable", '--allow-running-insecure-content',
        "--ignore-certificate-errors",
        # "--window-size=1920,{height}",
        # "--hide-scrollbars",
        # '--proxy-server=socks5://127.0.0.1:9050',
        # ]
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

    # driver.find_element_by_xpath("//img[@alt='" + str(title) + "']").click()
    # driver.implicitly_wait(30)

    page_width = driver.execute_script('return document.body.parentNode.scrollWidth') + 350
    page_height = driver.execute_script('return document.body.parentNode.scrollHeight') 
    driver.set_window_size(page_width, page_height)

    driver.save_screenshot(image_fname)

    driver.quit()
    return image_fname

# /Users/macbookpro/workspace/chromedriver

# browser.current_url
def KIA():

    kia_url = "https://www.kia.com/kr/event/progress-list.html"
    page_url = kia_url
    ##### 자바스크립트 페이지이므로 selenium 이용
    settings = {}
    settings['MAX_RETRIES'] = 3
    # settings['CHROME_PROXY'] = '127.0.0.1:9050'
    settings['CHROME_OPTIONS'] = ["--no-sandbox", "--disable-dev-shm-usage", "--disable-extensions", "--disable-gpu",
        "--disable-setuid-sandbox", "--ignore_ssl", "--dns-prefetch-disable", '--allow-running-insecure-content',
        "--ignore-certificate-errors",
        # '--proxy-server=socks5://127.0.0.1:9050',
        ]
        # "--headless"]
    settings['CHROME_EXCUTE']  = "/Users/macbookpro/workspace/chromedriver"
    settings['DO_SAVE_HTML'] = True

    options = webdriver.ChromeOptions()
    for opt in settings['CHROME_OPTIONS']:
        options.add_argument(opt)
    options.add_argument("user-agent={}".format('Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'))

    driver = webdriver.Chrome(EXCUTABLE_PATH, options=options) # executable path
    driver.implicitly_wait(30)

    kia_get = driver.get(page_url)

    kia_content = driver.page_source

    print(" requests complete")
    soup = BeautifulSoup(kia_content, features="html.parser") # from_encoding='cp949'
    kia_event = db["kia_event"]

    #####content#####

    # html 보기 및 저장
    
    presoup = soup.prettify()
    # print(presoup)
    f = open('kia_event.html', 'w', -1, 'utf-8')
    f.write(presoup)
    f.close()
    print('기아자동차 이벤트 페이지 저장완료!')

    content = soup.find('ul', {'class':'bbs_type2'})

    for event in content.find_all('li', {'class':'bbs_li ng-scope'}):
        title = event.find('strong', {'class':'bbs_tit ng-binding'}).get_text()
        adate = event.find('div', {'class':'bbs_date'})
        date = adate.find('span').get_text()
        id = crc32(title.encode()) #PK를 만들어주기 위해 title을 crc32로 인코딩함

        driver.find_element_by_xpath("//img[@alt='" + str(title) + "']").click()
        driver.implicitly_wait(30)

        link = driver.current_url
        driver.quit()

        print(id)
        print(title)
        print(date)
        print(link)

        # 이미지 파일 경로설정
        image = "{}_{}.png".format(sitename, id)

        try:
            kia_event.insert_one({"_id":id, "title":title, "date":date, "image":image})
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

        
         
        kia_url = "https://www.kia.com/kr/event/progress-list.html"
        page_url = kia_url
        ##### 자바스크립트 페이지이므로 selenium 이용
        settings = {}
        settings['MAX_RETRIES'] = 3
        # settings['CHROME_PROXY'] = '127.0.0.1:9050'
        settings['CHROME_OPTIONS'] = ["--no-sandbox", "--disable-dev-shm-usage", "--disable-extensions", "--disable-gpu",
            "--disable-setuid-sandbox", "--ignore_ssl", "--dns-prefetch-disable", '--allow-running-insecure-content',
            "--ignore-certificate-errors",
            # '--proxy-server=socks5://127.0.0.1:9050',
            # ]
            "--headless"]
        settings['CHROME_EXCUTE']  = "C:\\Users\\ys\\.vscode\\python_workspace\\chromedriver"
        settings['DO_SAVE_HTML'] = True

        options = webdriver.ChromeOptions()
        for opt in settings['CHROME_OPTIONS']:
            options.add_argument(opt)
        options.add_argument("user-agent={}".format('Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'))

        driver = webdriver.Chrome(EXCUTABLE_PATH, options=options) # executable path
        driver.implicitly_wait(30)

        driver.get(page_url)


    # for event in eventlist.find_all('li'): # 각각 하나하나의 이벤트
    #     alink = event.find('a')
    #     link = alink['href']

    #     text = event.find('div') # text 정보수집
    #     title = ''
    #     target = ''
    #     date = ''
    #     if(text.find('<p class="title">')!=-1):
    #         # print(text)
    #         title = text.find('b').get_text()
    #     if(text.find('<p class="info">')!=-1):
    #         target = text.find('span').get_text()
    #         date = text.find('span', {'class':'num'}).get_text()

    #     id = crc32(title.encode()) #PK를 만들어주기 위해 title을 crc32로 인코딩함

    #     print(id)
    #     print(title)
    #     print(target)
    #     print(date)

    #     # 이미지 파일 경로설정
    #     image = "{}_{}.png".format(sitename, id)
        

    return

 
if __name__ == '__main__':
    #print ("My Tor IP :", requests.get(p_ipcheck_url, proxies=proxies, headers=headers).text)
    print("KIA")
    KIA()
