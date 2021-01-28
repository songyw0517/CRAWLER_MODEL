# CRAWLER_MODEL
## 동기
COMTRIS 프로젝트를 시작하면서 크롤러를 다루게 되었다. 프로젝트를 할 때에는 기능을 수행하는 것에 초점을 두었기 때문에 코드가 많이 더러웠다.
언제든지 크롤러를 사용하기 위해서는 해당 코드를 정리할 필요성을 느끼고 코드리뷰를 하게 되었다.

# WEB CRAWLER
웹 크롤러(web crawler)는 조직적, 자동화된 방법으로 월드 와이드 웹을 탐색하는 컴퓨터 프로그램이다.

웹 크롤러가 하는 작업을 '웹 크롤링'(web crawling) 혹은 '스파이더링'(spidering)이라 부른다. 검색 엔진과 같은 여러 사이트에서는 데이터의 최신 상태 유지를 위해 웹 크롤링한다. 웹 크롤러는 대체로 방문한 사이트의 모든 페이지의 복사본을 생성하는 데 사용되며, 검색 엔진은 이렇게 생성된 페이지를 보다 빠른 검색을 위해 인덱싱한다. 또한 크롤러는 링크 체크나 HTML 코드 검증과 같은 웹 사이트의 자동 유지 관리 작업을 위해 사용되기도 하며, 자동 이메일 수집과 같은 웹 페이지의 특정 형태의 정보를 수집하는 데도 사용된다

COMTRIS 프로젝트에서도 AI학습을 위한 방대한 데이터가 필요했기 때문에 크롤러 사용이 불가피했다.

# CODE REVIEW
## crawler_model.py
- 크롤러의 클래스를 정의했다.

``` python
class crawler:
    header = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)\
            AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
            "Accept":"text/html,application/xhtml+xml,application/xml;\
            q=0.9,imgwebp,*/*;q=0.8"
        }
    # 생성자
    def __init__(self,  url):
        super(crawler, self).__init__()
        self.url = url 
        self.domain = self.url.split('/')[0] + '//' + self.url.split('/')[2] 
        self.driver = requests.get(self.url, verify = False, headers = self.header)
        self.html = self.driver.content.decode('euc-kr', 'replace') # encoding to korean
        # 한글 깨짐 방지, https://blog.naver.com/PostView.nhn?blogId=redtaeung&logNo=221904432971    
        # utf-8이 아닌 euc-kr 변경시 작동 되었다.
        self.page = BeautifulSoup(self.html, 'html.parser')
    def setUrl(self, url):
        self.url = url
        self.domain = self.url.split('/')[0] + '//' + self.url.split('/')[2]
        self.driver = requests.get(self.url, verify = False, headers = self.header)
        self.html = self.driver.content.decode('euc-kr', 'replace')
        self.page = BeautifulSoup(self.html, 'html.parser')
    def getPage(self):
        return self.page
    def getUrl(self):
        return self.url
    def getDomain(self):
        return self.domain
    def select(self, path):
        return self.page.select(path)
```
## crawler class
### data
- url
- domain
- driver
- html
- page
### methods
- setUrl("url") : 
> url을 재설정한다.
> 
> url을 통해 domain, drvier, html, page 또한 같이 재설정한다.
- getPage()
- getUrl()
- getDomain()
- select("path")
> html의 path를 통해서 크롤링할 데이터를 select하여 반환한다.

# 마무리
crawler_model.py의 crawler 클래스 외에 

crawler를 상속받은 danawa_pc_crawler 클래스가 있다. 

나중에 crawler을 다룰 기회가 다시 생긴다면 

참고하여 클래스를 작성하면 좋을 듯하다.