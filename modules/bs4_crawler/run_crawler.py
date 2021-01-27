import os
import time
import requests
import numpy
from bs4 import BeautifulSoup
from pymongo import *
from modules.bs4_crawler.crawler_model import * # modules/bs4_crawler/crawler_model.py의 *

def crawler_run():
    
    # ------------- init part --------------
    myclient = MongoClient(os.getenv("MONGODB_URI")) # 환경변수 적용
    db = myclient['CRAWLER']
    col = db["master_config"]
    # db로 부터 'key' : quote_cnt인 document의 'value'의 값을 찾음
    page_num = col.find_one({'key':'quote_cnt'})['value'] 
    base_url = "http://shop.danawa.com/pc/?controller=estimateDeal&methods=lists&registerSectionSeq=6&page={}"
    current_url = base_url.format(page_num)
    Crawler = danawa_pc_crawler(current_url)
    Crawler_sub = danawa_pc_crawler(current_url)
    # ------------- run part -------------- 
    
    while True:
        time.sleep(numpy.random.randint(1,3)) # 1~3사이의 랜덤한 sec 만큼 sleep
        # -> 사람이 하는 것처럼 하여 서버가 벤되는 것을 막기 위함
        page_num += 1
        col.update_one({"key":'quote_cnt'}, {'$set':{'value':page_num}}) # db quote_cnt 갱신
        current_url = base_url.format(page_num)
        Crawler.setUrl(current_url) # url 재설정
        rows = len(Crawler.select('.setpc_bbs_tbl>tbody>tr')) # rows 갯수
        print("page_num = ", page_num)
        if not rows:
            print("빈 페이지 입니다.")
            break
        else:
            for i in range(rows): # Rows 갯수만큼 반복
                try:
                    date = Crawler.getDate(i)
                    name = Crawler.getName(i)
                    title = Crawler.getTitle(i).split("\n")
                    # 비밀글을 걸러내기 위해서 list로 만듬. 비밀글이면 ['title', '비밀글']로 나옴
                    aver_price = Crawler.getAverPrice(i)
                    status = Crawler.getStatus(i)
                    link = Crawler.getDomain() + '/pc/' + Crawler.getLink(i)
                    id = Crawler.getLink(i)
                    id = int(id[id.rfind("=")+1 : len(id)].strip())
                    print(id, date, name, title, aver_price, status, link)
                except Exception as e:
                    print("터짐")
                    print(e)
                    continue
                else:
                    if '비밀글' in title:
                        print("비밀글이므로 pass")
                        continue
                    else:
                        try:
                            Crawler_sub.setUrl(link) # sub url로 설정
                            time.sleep(numpy.random.randint(1,3)) # 3~5사이의 랜덤한 sec 만큼 sleep
                        except Exception as e:
                            print("link 접속 실패")
                            print(e)
                            continue
                        else : # link 접속 성공 -> 키 가져오기
                            try : 
                                keys = Crawler_sub.getKey() # key를 받음
                                # print("keys = ", keys)
                                result, pass_ = Crawler_sub.getDict(keys, id, status) # 사전 형식으로 데이터를 받아옴
                                key_val = Crawler_sub.KeysValidation(keys)
                                # pass_ 는 1은 문제가 없는것, key_val도 True가 문제가 없는것

                                if pass_ and key_val: # 문제 없음
                                    result.update({'id':id, 'pass':1}) # 문제없으므로 1
                                    Crawler_sub.insert_one(result) # db에 삽입
                                    print("삽입 완료, result = ", result)
                                else : # 문제 있음
                                    result.update({'id':id, 'pass':0}) # 문제있으므로 0
                                    Crawler_sub.insert_one(result) # db에 삽입
                                    print("부품없음 삽입 완료, result = ", result)

                            except Exception as e:
                                continue
                                # print('getting Key Error')
                                # print(e)
                    
    # ------------- test part --------------
    '''
    test = danawa_pc_crawler(base_url, page_num)
    print("test")
    page_num = 1
    test.setPageNum(1)
    print(len(test.select('.setpc_bbs_tbl>tbody>tr')))
    '''



