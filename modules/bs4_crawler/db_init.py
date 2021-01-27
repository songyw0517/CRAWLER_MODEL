import os
from pymongo import *

def db_init():
    myclient = MongoClient(os.getenv("MONGODB_URI")) 
    ''' 환경변수 적용, CRAWLER_URI : mongodb://localhost:27017 추가
    찾아보니 os.environ[] 보다 os.getenv()을 통해 keyError를 다룬다고 한다.
    https://ohgyun.com/697
    
    ++ 윈도우에서 환경변수를 생성하고 적용한 후에 코드 편집기를 재실행해야 적용이 된다.
    '''
    db = myclient['CRAWLER']
    col = db["master_config"] # 필요한 변수 DB로 관리

    cnt_check = col.find_one({'key': 'quote_cnt'})
    if not cnt_check:
        col.insert_one({'key':'quote_cnt', 'value': 0})
    
    print("bs4 init complete")
if __name__ == '__main__':
    db_init()