import os
from pymongo import *

def db_init():
    myclient = MongoClient(os.environ["CRAWLER_URI"]) # 환경변수 적용, CRAWLER_URI : mongodb://localhost:27017 추가
    db = myclient['CRAWLER']
    col = db["master_config"] # 필요한 변수 DB로 관리

    cnt_check = col.find_one({'key': 'quote_cnt'})
    if not cnt_check:
        col.insert_one({'key':'quote_cnt', 'value': 0})
    
    print("bs4 init complete")
if __name__ == '__main__':
    db_init()