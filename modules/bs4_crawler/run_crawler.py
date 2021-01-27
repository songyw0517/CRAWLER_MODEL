import os
import time
import requests
import numpy
from bs4 import BeautifulSoup
from pymongo import *
from crawler_model import *
def crawler_run():
    
    # ------------- init part --------------
    myclient = MongoClient(os.environ["CRAWLER_URI"])
    db = myclient['CRAWLER']
    col = db["master_config"]
    # db로 부터 'key' : quote_cnt인 document의 'value'의 값을 찾음
    page_num = col.find_one({'key':'quote_cnt'})['value'] 
    base_url = "http://shop.danawa.com/pc/?controller=estimateDeal&methods=lists&registerSectionSeq=6&page={}"
    Crawler = crawler(base_url, page_num)
    
    # ------------- run part -------------- 
    '''
    while True:
        # time.sleep(numpy.random.randint(3,5)) # 3~5사이의 랜덤한 sec 만큼 sleep
        # -> 사람이 하는 것처럼 하여 서버가 벤되는 것을 막기 위함
        page_num += 1
        col.update_one({"key":'quote_cnt'}, {'$set':{'value':page_num}}) # db quote_cnt 갱신
        Crawler.setPageNum(page_num)
    '''
    # ------------- test part --------------
    
    print("test the print")



