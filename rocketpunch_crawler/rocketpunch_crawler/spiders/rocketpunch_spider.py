import scrapy
import requests
from bs4 import BeautifulSoup
import json
from rocketpunch_crawler.items import RocketpunchCrawlerItem

class RocketpunchSpider(scrapy.Spider):
    name = "Rocketpunch"
    allowed_domains = ['https://www.rocketpunch.com']
    
    def __init__(self, specialty="python", tag="데이터", page=1, **kwargs):
        url_for_get_page = "https://www.rocketpunch.com/api/jobs/template?q=&specialty={}&tag={}&page={}".format(specialty, tag, page)
        response = requests.get(url_for_get_page)
        data = response.json()['data']['template']
        dom = BeautifulSoup(data, "html.parser")
        total_pages = dom.select("div.ui.pagination.menu > div.tablet.computer.large.screen.widescreen.only > a")[-1].text

        self.start_urls = []

        for page in range(1,int(total_pages)+1):
            url = "https://www.rocketpunch.com/api/jobs/template?q=&specialty={}&tag={}&page={}".format(specialty, tag, page)
            self.start_urls.append(url)           
        super().__init__(**kwargs)
        
        
    def parse(self, response):
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