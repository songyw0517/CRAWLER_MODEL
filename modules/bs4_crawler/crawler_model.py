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
    - page_num
    - base_url
    '''
    header = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)\
            AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
            "Accept":"text/html,application/xhtml+xml,application/xml;\
            q=0.9,imgwebp,*/*;q=0.8"
        }
    # 생성자
    def __init__(self, base_url, page_num):
        super(crawler, self).__init__()
        self.base_url = base_url
        self.url = base_url.format(page_num) # init crawler url
        self.domain = self.url.split('/')[0] + '//' + self.url.split('/')[2] # init crawler domain
        self.driver = requests.get(self.url, verify = False, headers = self.header)
        self.html = self.driver.content.decode('euc-kr', 'replace') # encoding to korean
        # 한글 깨짐 방지, https://blog.naver.com/PostView.nhn?blogId=redtaeung&logNo=221904432971    
        # utf-8이 아닌 euc-kr 변경시 작동 되었다.
        self.page = BeautifulSoup(self.html, 'html.parser')
    def setPageNum(self, page_num):
        '''base_url은 유지된 상태에서 page_num만 바뀐 경우
        -> page_num, url, driver, html, page 변경
        '''
        self.page_num = page_num
        self.url = self.base_url.format(page_num)
        self.driver = requests.get(self.url, verify = False, headers = self.header)
        self.html = self.driver.content.decode('euc-kr', 'replace') # encoding to korean
        self.page = BeautifulSoup(self.html, 'html.parser')
    def setBaseUrl(self, base_url):
        ''' base_url이 바뀐 경우
        -> base_url, url, domain, page_num, driver, html, page 변경
        '''
        self.base_url = base_url
        self.page_num = 1 # 첫번째 페이지로 지정
        self.url = self.base_url.format(self.page_num)
        self.driver = requests.get(self.url, verify = False, headers = self.header)
        self.html = self.driver.content.decode('euc-kr', 'replace') # encoding to korean
        self.page = BeautifulSoup(self.html, 'html.parser')
        
    def getPage(self):
        return self.page
    
    def select(self, path):
        return self.page.select(path)

class danawa_pc_crawler(crawler):
    def __init__(self, base_url, page_num):
        super().__init__(base_url, page_num)
        self.myclient = MongoClient(os.environ["CRAWLER_URI"])
        self.db = self.myclient['CRAWLER']
        self.col = self.db["CRAWLER_TEST"] # CRAWLER_TEST의 COLLECTION 사용

