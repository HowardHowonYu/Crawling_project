import scrapy
import requests
from scrapy.http import TextResponse
import time

from job_hunter.items import JobHunterItem


class Spider(scrapy.Spider):
    name = "JobkoreaCrawler"
    allow_domain = ["https://www.jobkorea.co.kr/"]
    start_urls = []
   
    # 아규먼트를 받을수 있게 지정해 줬습니다.
    # 잡코리아는 언어 설정, 특기등 설정값을 디테일하게 주지 못합니다.
    # careerType =1 은 신입을 말합니다. 추후 경력직 까지 크롤링 할떄 생성자 함수에 아규먼트를 추가할수 있습니다.
    def __init__(self, serach_keyword="데이터 분석", careerType=1, page=1, **kwargs):
    
        self.start_urls = ["https://www.jobkorea.co.kr/Search/?stext={}&careerType={}&tabType=recruit&Page_No={}".format(serach_keyword,careerType,page)]    
        
        super().__init__(**kwargs)

    
    def parse(self, response):
        # 크롤링시 잡코리아에서 ip를 차단해 버리기 떄문에 딜레이를 걸어줬습니다.
        time.sleep(5)
        total_pages = int(response.xpath('//*[@id="content"]/div/div/div[1]/div/div[2]/div[2]/div/div[3]/ul/li[2]/span/text()')[0].extract())
        # 나중에 사람인이나 다른 사이트들 한 spider에서 크롤링 하려면 어떻게 할지 고민
        for page in range(1, total_pages +1):                        
            # 문자열의 마지막 글자만 잡아서 total_pages의 숫자만큼 url을 만들고 yield로 get_content()함수에 던져줍니다.
            page_url = self.start_urls[0][:-1]+"{}".format(page)
            yield scrapy.Request(page_url, callback=self.get_content)
        
    
   
    def get_content(self, response):
    # 크롤링시 잡코리아에서 ip를 차단해 버리기 떄문에 딜레이를 걸어줬습니다.
        time.sleep(5)
        links = response.xpath('//*[@id="content"]/div/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li/div/div[2]/a/@href').extract()
        # 이과정에서 각 페이지 별로 가지고 있는 구인 공고들의 링크를 만들어 yield로 get_details()함수에 던져줍니다.
        links = ["http://www.jobkorea.co.kr/" + link for link in links]   
        for link in links:
            yield scrapy.Request(link, callback=self.get_details)
      
      
    def get_details(self, response):
        time.sleep(5)
        item = JobHunterItem()   
        
        item["company_name"] = response.xpath('//*[@id="container"]/section/div/article/div[1]/h3/span/text()')[0].extract().strip()
        try:
            item["deadline"] = response.xpath('//*[@id="tab02"]/div/article[1]/div/dl[2]/dd[2]/span/text()')[0].extract()[5:] + " 마감"
        except:
            item["deadline"] = "수시채용"
            
        item['link'] = response.url
        
        item["position"] = response.xpath('//*[@id="container"]/section/div/article/div[1]/h3/text()')[1].extract().strip()
        
        item['location'] = ",".join(response.xpath('//*[@id="container"]/section/div/article/div[2]/div/dl/dd/a/text()').extract())
        
        item["keyword"] = response.xpath('//*[@id="artKeywordSearch"]/ul/li/button/text()').extract()[:-1]
        
        
        # 구인 공고 링크 안으로 들어가 더 자세한 정보를 가져옵니다.
        url = "http://www.jobkorea.co.kr" + response.xpath('//*/article[contains(@class, "artReadCoInfo") and contains(@class, "divReadBx")]/div/div/p/a/@href')[0].extract()
        
        req = requests.get(url)
        response_detail_page = TextResponse(req.url,body=req.text,encoding='utf-8')
        
        item["business"] = response_detail_page.xpath('//*[@id="company-body"]/div[1]/div[1]/div/div/div[9]/div[2]/div/div/text()')[0].extract()
           
        try:
            item["salary_condition"] = response_detail_page.xpath('//*[@id="company-body"]/div[1]/div[1]/div/div/div[8]/div[2]/div/div/div/div/text()')[0].extract()
        except:
            item["salary_condition"] = "회사 내규에 따름 - 연봉 협의"
        
        
        yield item
 