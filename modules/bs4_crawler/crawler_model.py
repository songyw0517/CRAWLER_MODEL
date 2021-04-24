import sys
import requests
import re
import datetime
import os
from pymongo import *
from bs4 import BeautifulSoup

class crawler:
    '''
    data
    - headers # 고정 값
    - driver
    - html
    - url
    - domain
    - page
    '''
    header = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)\
            AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
            "Accept":"text/html,application/xhtml+xml,application/xml;\
            q=0.9,imgwebp,*/*;q=0.8"
        }
    # 생성자
    def __init__(self, url):
        super(crawler, self).__init__()
        self.url = url # init crawler url
        self.domain = self.url.split('/')[0] + '//' + self.url.split('/')[2] # init crawler domain
        self.driver = requests.get(self.url, verify = False, headers = self.header)
        self.html = self.driver.content.decode('utf-8', 'replace') # encoding to korean
        # 한글 깨짐 방지, https://blog.naver.com/PostView.nhn?blogId=redtaeung&logNo=221904432971    
        # utf-8이 아닌 euc-kr 변경시 작동 되었다.
        self.page = BeautifulSoup(self.html, 'html.parser')
    def setUrl(self, url):
        ''' url 변경
        -> url, domain, driver, html, page 변경
        '''
        self.url = url
        self.domain = self.url.split('/')[0] + '//' + self.url.split('/')[2] # init crawler domain
        self.driver = requests.get(self.url, verify = False, headers = self.header)
        self.html = self.driver.content.decode('euc-kr', 'replace') # encoding to korean
        self.page = BeautifulSoup(self.html, 'html.parser')
          
    def getPage(self):
        return self.page
    def getUrl(self):
        return self.url
    def getDomain(self):
        return self.domain
    def select(self, path):
        return self.page.select(path)
    
class blog_crawler(crawler):
    def __init__(self, url):
        super().__init__(url)
    def getText(self):
        return self.page.select('#div_\$\{article\.articleNo\} .tt_article_useless_p_margin p')[1].text

class danawa_pc_crawler(crawler):
    def __init__(self, url):
        super().__init__(url)
        self.myclient = MongoClient(os.getenv("MONGODB_URI")) # 환경변수 적용
        self.db = self.myclient['CRAWLER']
        self.col = self.db["CRAWLER_TEST"] # CRAWLER_TEST의 COLLECTION 사용
    
    def getDate(self, index):
        return self.page.select('.setpc_bbs_tbl>tbody>tr>.date')[index].text
    def getName(self, index):
        return self.page.select('.setpc_bbs_tbl>tbody>tr>.name')[index].text
    def getTitle(self, index):
        return self.page.select('.setpc_bbs_tbl>tbody>tr>.title')[index].text.strip()
    def getAverPrice(self, index):
        return self.page.select('.setpc_bbs_tbl>tbody>tr>.aver_price')[index].text
    def getStatus(self, index):
        return self.page.select('.setpc_bbs_tbl>tbody>tr>.status')[index].text
    def getLink(self, index):
        return self.page.select('.setpc_bbs_tbl>tbody>tr>.title a')[index]['href']
    def getRowsToNumber(self):
        return len(self.page.select('.setpc_bbs_tbl>tbody>tr'))
    def getKey(self):
        keys = []
        temp_key = list(map(lambda page:page.text, self.page.select('.tbl_t3>tbody>tr>.srt')))
        for i in temp_key:
            if(i == 'CPU'):
                keys.append("CPU")
            elif(i == '메인보드'):
                keys.append('M/B')
            elif(i == '메모리'):
                keys.append('RAM')
            elif(i == '그래픽카드'):
                keys.append('VGA')
            elif(i == 'SSD'):
                keys.append('SSD')
            elif(i == '파워'):
                keys.append('POWER')
            else :
                keys.append(i)
        return keys
    def KeysValidation(self, keys):
        flag = True # 문제 없음
        empty_part = []
        for require in ["CPU", "M/B", "RAM", "SSD", "VGA", "POWER"]:
            if require not in keys:
                flag = False # 문제 있음(부품 없음)
                empty_part.append(require)
        return flag
    def getDict(self, keys, id, status):
        # print("getDict")
        result = {'id':id, 'status':status} # id 추가하여 초기화
        # price = {}
        pass_ = 1

        for idx, key in enumerate(keys):
            value = self.page.select('.tbl_t3>tbody>tr>.tit')[idx].text
            value = value.strip().split('\n')
            if key == "CPU": 
                result["CPU"] = value[0]
            elif key == "M/B":
               result["M/B"] = value[0]
            elif key == "RAM":
               result["RAM"] = value[0]
            elif key == "SSD":
                result["SSD"] = value[0]
            elif key == "VGA":
                result["VGA"] = value[0]
            elif key == "POWER":
                result["POWER"] = value[0]

        # 구매 날짜 긁기 -> date type으로 변경
        shop_date = re.search("\d{4}.\d{2}.\d{2}\s\s\d{2}:\d{2}", self.page.select('.u_info>.date')[0].text).group()
        shop_year = int(shop_date[0:4].strip())
        shop_month = int(shop_date[5:7].strip())
        shop_day = int(shop_date[8:10].strip())
        shop_date = datetime.datetime(shop_year, shop_month, shop_day)
        crawl_date = datetime.datetime.now()
        result.update({'id' : id, "crawl_date" : crawl_date, 'shop_date' : shop_date})

        return result, pass_
    # DB methods
    def insert_one(self, document):
        self.col.insert_one(document) # self.col에 삽입

    # 소멸자
    def __del__(self):
        self.myclient.close()