import scrapy
import requests
from scrapy.http import TextResponse
import time
# 보안문자 입력하라는 메세지 떳음


from jobkorea_crawler.items import JobkoreaCrawlerItem


class Spider(scrapy.Spider):
    name = "JobkoreaCrawler"
    allow_domain = ["https://www.jobkorea.co.kr/"]
    start_urls = []
   
    url = "http://www.jobkorea.co.kr/Search/?stext=%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%B6%84%EC%84%9D&careerType=1&tabType=recruit&Page_No=1"
    req_for_page = requests.get(url)
    response_for_page = TextResponse(req_for_page.url, body=req_for_page.text, encoding="utf-8")
    total_links = int(response_for_page.xpath('//*[@id="content"]/div/div/div[1]/div/div[2]/div[1]/p/strong/text()')[0].extract())
    pages_num = total_links // 20
    for page in range(1,pages_num+1):
        page_url = url[:-1]+"{}".format(page)
        start_urls.append(page_url)
    
    # 잡코리아 크롤링 보안코드 입력하라 그러고 ip 막겠다고 하는데 time sleep 걸면서 계속 시도해 봐도 될지?
    def parse(self,response):
        time.sleep(60)
        links = response.xpath('//*[@id="content"]/div/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li/div/div[2]/a/@href').extract()
        links = ["http://www.jobkorea.co.kr/" + link for link in links]   
        for link in links:
            yield scrapy.Request(link,callback=self.get_details)
      

    def get_details(self,response):
        time.sleep(10)
        item = JobkoreaCrawlerItem()   
        
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
            item["job_condition"] = response_detail_page.xpath('//*[@id="company-body"]/div[1]/div[1]/div/div/div[8]/div[2]/div/div/div/div/text()')[0].extract()
        except:
            item["job_condition"] = "회사 내규에 따름 - 연봉 협의"
            
        item["keyword"] = response.xpath('//*[@id="artKeywordSearch"]/ul/li/button/text()').extract()[:-1]
        
        yield item
 