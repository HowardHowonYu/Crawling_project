import scrapy
from scrapy.selector import Selector
import requests
from bs4 import BeautifulSoup
import json
from rocketpunch_crawler.items import RocketpunchCrawlerItem

class RocketpunchSpider(scrapy.Spider):
    name = "Rocketpunch"
    allowed_domains = ['https://www.rocketpunch.com']
    start_urls = []
    
    # 검색어 마다 페이지가 다르기 때문에, 총 페이지 수를 먼저 체크하고 각 페이지의 URL을 'start_urls' 변수에 리스트 형태로 담는다.
    url = "https://www.rocketpunch.com/api/jobs/template?page=&q=&specialty=Python&tag=%EB%8D%B0%EC%9D%B4%ED%84%B0"
    response = requests.get(url)
    data = response.json()['data']['template']
    dom = BeautifulSoup(data, "html.parser")
    total_pages = dom.select("div.ui.pagination.menu > div.tablet.computer.large.screen.widescreen.only > a")[-1].text
    
    for page in range(1,int(total_pages)+1):
        url = "https://www.rocketpunch.com/api/jobs/template?page={}&q=&specialty=Python&tag=%EB%8D%B0%EC%9D%B4%ED%84%B0".format(page)
        start_urls.append(url)
    
    
# 멀티 쓰레드로 돌리려면 __init__ 안에서 start_url을 찾는짓을 해주자.

# 수업 참조
#  def parse(self,response):
#         selector = '//*[@id="gBestWrap"]/div/div[3]/div[2]/ul/li/a/@href'
#         links = links = response.xpath(selector).extract()
#         for link in links:
#             yield scrapy.Request(link,callback=self.get_content)
#             # 여기서 link로 Request한걸 콜백 함수get_content로 던져준다


# 순서대로 저장하려면 rank값 줘서 나중에 소팅해보자
    
    def __init__(self):
        # 기존 Spider 클래스의 생성자를 초기화 해준다.
        scrapy.Spider.__init__(self)
        
        company_name = scrapy.Field()
        deadline = scrapy.Field()
        business  = scrapy.Field()
        link = scrapy.Field()
        position = scrapy.Field()
        job_condition = scrapy.Field()
        keyword = scrapy.Field()

    
        
    def parse(self, response):
#       response = requests.get(url)
        jsonresponse = json.loads(response.body)
        data = jsonresponse['data']['template']       
        dom = BeautifulSoup(data, "html.parser")

        root = dom.select('#company-list > div.company.item > div.content')
        positions = dom.select('#company-list > div.company.item > div.content > div.company-jobs-detail')

        for i in range(len(root)):
            len_of_positions = len(positions[i].select('div:nth-child(1) > a.nowrap')) 
            
            for j in range(len_of_positions):
                link = "https://www.rocketpunch.com" + positions[i].select('div:nth-child(1) > a.nowrap')[j].get('href') 
                response = requests.get(link)
                dom_for_skills = BeautifulSoup(response.text,"html.parser")    
                
                item = RocketpunchCrawlerItem()
                item["company_name"] = root[i].select('div.company-name > a > h4 > strong')[0].text
                item["business"] = root[i].select('div.description')[0].text.strip('\xa0')
                item["position"] = positions[i].select('div:nth-child(1) > a.nowrap')[j].text
                item["link"] = link
                item["salary_condition"] = positions[i].select('div.job-detail > div:nth-child(1) > span')[j].text
                item["deadline"] = positions[i].select('div.job-detail > div.job-dates > span:nth-child(1)')[j].text.strip(' \n').replace("/",".")
                item["keyword"] = ", ".join([a.text for a in dom_for_skills.select('div .job-specialties > a ')])
                # <br\>로 나누어져 있기 때문에, 처음부터 끝까지 1칸씩 간격을 두고 찾아내면 지역이 몇개건 상관없이 가져올수 있음
                item['location'] = ", ".join(dom_for_skills.select('#wrap > div.four.wide.job-infoset.column > div > div:nth-child(3) > div > div:nth-child(2) > div.content')[0].contents[::2]).strip()
                yield item