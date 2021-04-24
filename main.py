from bs4 import BeautifulSoup
from modules.bs4_crawler.crawler_model import * # modules/bs4_crawler/crawler_model.py의 *
import os
import time
import requests
import numpy


if __name__ == '__main__':
   #run.crawler_run()
   blog_url = "https://blog.daum.net/santaclausly/11793674"
   crawler = blog_crawler(blog_url)
   print(crawler.getText())