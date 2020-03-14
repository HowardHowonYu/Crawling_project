import scrapy
import requests
from scrapy.http import TextResponse
import time

from job_hunter.items import JobHunterItem


class Spider(scrapy.Spider):
   
    name = "SaraminCrawler"
    allow_domain = ["http://www.saramin.co.kr/"]

    def __init__(self, searchword="데이터사이언스", **kwargs):

        self.start_urls = ["http://m.saramin.co.kr/search?searchType=search&searchword={}".format(searchword)]

        super().__init__(**kwargs)



    def parse(self, response):

         total_pages = response.xpath('//*[@class="pagiNation"]/a[last()]/text()')[0].extract()

         for i in range(1,int(total_pages)+1):
            url = self.start_urls[0] + "&page={}".format(i)
            req = requests.get(url)
            response = TextResponse(req.url, body=req.text, encoding="utf-8")
            links = response.xpath('//*[@id="recruit_result"]/ul/li/div/a/@href').extract()
            links = ["http://m.saramin.co.kr"  + link + "&t_ref=search&t_ref_content=generic" for link in links]   
            for link in links:
                yield scrapy.Request(link, callback=self.get_content)

       


    def get_content(self,response):
        item = JobHunterItem()  
       
        result = response.xpath('//*[@id="card_set"]/div[1]/div/div[1]/div/span/span/text()').extract()

        if result:
            item['company_name'] = result[0]
        else :
            item['company_name'] = response.xpath('//*[@id="card_set"]/div[1]/div/div[1]/div/span/a/text()')[0].extract()
            

        try : 
            item['business'] = response.xpath('//*[@id="card_set"]/div[1]/div/section[4]/div/div[2]/dl[2]/dd/div/text()')[0].extract().strip()

        except:
            item['business'] = "회사 정보 없음"


        item['position'] = response.xpath('//*[@id="card_set"]/div[1]/div/div[1]/div/h2/text()')[0].extract().strip()

        item['link'] = response.xpath('//*[@class="footer_link"]/li/a/@href')[2].extract()
     
        
        salary_result = response.xpath('//*[@class="card_cont wrap_recruit_view"]/section[@class="section_view section_basic_view"]/div[@class="wrap_info_job"]/dl[2]/dd/text()')[0].extract().strip()
        if salary_result:
                item["salary_condition"] = salary_result
        else:
                item["salary_condition"] = "면접 후 결정(조건 상이)"
       

        item['location'] = response.xpath('//*[@class="card_cont wrap_recruit_view"]/section[@class="section_view section_basic_view"]/div[@class="wrap_info_job"]/dl[3]/dd/div/text()')[0].extract().strip()

        deadline = response.xpath('//*[@class="card_cont wrap_recruit_view"]/section[@class="section_view section_basic_view"]/div[@class="wrap_info_job"]/dl[1]/dd/span[1]/text()')[0].extract().strip()
        
        if deadline:
            item['deadline'] = deadline
        else:
            item['deadline'] = "상시 채용"
        
        item['keyword'] = str(response.xpath('//*[@class="list_relation_tag"]/li/a/text()').extract()).strip("[]''")

        yield item
