import scrapy
import requests
from scrapy.http import TextResponse
import time

from job_hunter.items import JobHunterItem


class Spider(scrapy.Spider):
    name = "JobkoreaCrawler"
    allow_domain = ["https://www.jobkorea.co.kr/"]
    start_urls = []
   
    def __init__(self, serach_keyword="데이터 분석", page=1, **kwargs):
    
        self.start_urls = ["http://www.jobkorea.co.kr/Search/?stext={}&careerType=1&tabType=recruit&Page_No={}".format(serach_keyword,page)]
    
        super().__init__(**kwargs)
            
    def parse(self, response):
        time.sleep(5)
        total_pages = int(response.xpath('//*[@id="content"]/div/div/div[1]/div/div[2]/div[2]/div/div[3]/ul/li[2]/span/text()')[0].extract())
        for page in range(1, total_pages +1):
            page_url = self.start_urls[0][:-1]+"{}".format(page)
            yield scrapy.Request(page_url,callback=self.get_content)
        
    # 잡코리아 크롤링 보안코드 입력하라 그러고 ip 막겠다고 하는데 time sleep 걸면서 계속 시도해 봐도 될지?
   
    def get_content(self, response):
        time.sleep(5)
        links = response.xpath('//*[@id="content"]/div/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li/div/div[2]/a/@href').extract()
        links = ["http://www.jobkorea.co.kr/" + link for link in links]   
        for link in links:
            yield scrapy.Request(link,callback=self.get_details)
      
      
    def get_details(self,response):
        time.sleep(5)
        item = JobHunterItem()   
        
        item["company_name"] = response.xpath('//*[@id="container"]/section/div/article/div[1]/h3/span/text()')[0].extract().strip()
        try:
            item["deadline"] = response.xpath('//*[@id="tab02"]/div/article[1]/div/dl[2]/dd[2]/span/text()')[0].extract()[5:] + " 마감"
        except:
            item["deadline"] = "수시채용"
            
        url = "http://www.jobkorea.co.kr" + response.xpath('//*/article[contains(@class, "artReadCoInfo") and contains(@class, "divReadBx")]/div/div/p/a/@href')[0].extract()
        
        req = requests.get(url)
        response_detail_page = TextResponse(req.url,body=req.text,encoding='utf-8')
        
        item["business"] = response_detail_page.xpath('//*[@id="company-body"]/div[1]/div[1]/div/div/div[9]/div[2]/div/div/text()')[0].extract()
        
        item['link'] = response.url
        
        item["position"] = response.xpath('//*[@id="container"]/section/div/article/div[1]/h3/text()')[1].extract().strip()

        try:
            item["salary_condition"] = response_detail_page.xpath('//*[@id="company-body"]/div[1]/div[1]/div/div/div[8]/div[2]/div/div/div/div/text()')[0].extract()
        except:
            item["salary_condition"] = "회사 내규에 따름 - 연봉 협의"
        
        item['location'] = ",".join(response.xpath('//*[@id="container"]/section/div/article/div[2]/div/dl/dd/a/text()').extract())
        
        item["keyword"] = response.xpath('//*[@id="artKeywordSearch"]/ul/li/button/text()').extract()[:-1]
        
        yield item
 


