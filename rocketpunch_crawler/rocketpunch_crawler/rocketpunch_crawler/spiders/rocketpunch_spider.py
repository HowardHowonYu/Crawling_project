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
    url = "https://www.rocketpunch.com/api/jobs/template?page=1&q=&specialty=Python&tag=%EB%8D%B0%EC%9D%B4%ED%84%B0%3E"
    response = requests.get(url)
    data = response.json()['data']['template']
    dom = BeautifulSoup(data, "html.parser")
    total_pages = dom.select("div.ui.pagination.menu > div.tablet.computer.large.screen.widescreen.only > a")[-1].text
    
    for page in range(1,int(total_pages)+1):
        url = "https://www.rocketpunch.com/api/jobs/template?page={}&q=&specialty=Python&tag=%EB%8D%B0%EC%9D%B4%ED%84%B0%3E".format(page)
        start_urls.append(url)
    
    
    
    
    def __init__(self):
        # 기존 Spider 클래스의 생성자를 초기화 해준다.
        scrapy.Spider.__init__(self)
        
        
        
    def parse(self, response):
#         response = requests.get(url)
        jsonresponse = json.loads(response.body)
        data = jsonresponse['data']['template']
        dom = BeautifulSoup(data, "html.parser")

        root = dom.select('#company-list > div.company.item > div.content')
        positions = dom.select('#company-list > div.company.item > div.content > div.company-jobs-detail')

        for i in range(len(root)):
            len_of_positions = len(positions[i].select('div:nth-child(1) > a.nowrap'))        
            for j in range(len_of_positions):
                item = RocketpunchCrawlerItem()
                item["company"] = root[i].select('div.company-name > a > h4 > strong')[0].text
                item["description"] = root[i].select('div.description')[0].text.strip('\xa0')
                item["service"] = root[i].select('div.nowrap.meta')[0].text.strip()
                item["position"] = positions[i].select('div:nth-child(1) > a.nowrap')[j].text
                item["link"] = "https://www.rocketpunch.com" + positions[i].select('div:nth-child(1) > a.nowrap')[j].get('href')
                item["salary"] = positions[i].select('div.job-detail > div:nth-child(1) > span')[j].text
                item["deadline"] = positions[i].select('div.job-detail > div.job-dates > span:nth-child(1)')[j].text.strip(' \n')
                yield item