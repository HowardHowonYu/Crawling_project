import scrapy
import requests
from bs4 import BeautifulSoup
import json
import datetime


from job_hunter.items import JobHunterItem

class RocketpunchSpider(scrapy.Spider):

    # 크롤러 이름 설정
    name = "Rocketpunch"
    allowed_domains = ['https://www.rocketpunch.com']
    
    # 생성자 함수에서 구인 목록의 전체 페이지수를 구하고, start_url에 담아준다
    def __init__(self, specialty="python", tag="데이터", page=1, **kwargs):
        self.start_urls = []   
        url_for_get_page = "https://www.rocketpunch.com/api/jobs/template?q=&specialty={}&tag={}&page={}".format(specialty, tag, page)    
        response = requests.get(url_for_get_page)         
        
        # json형태 변환 후 html코드가 담겨있는 str데이터 선택
        data = response.json()['data']['template']        
        
        # str데이터를 html로 파싱
        dom = BeautifulSoup(data, "html.parser")
        
        # select함수를 이용해 
        total_pages = dom.select("div.ui.pagination.menu > div.tablet.computer.large.screen.widescreen.only > a")[-1].text
  
        for page in range(1,int(total_pages)+1):
            url = "https://www.rocketpunch.com/api/jobs/template?q=&specialty={}&tag={}&page={}".format(specialty, tag, page)
            self.start_urls.append(url)
        
        super().__init__(**kwargs)
        
    
    # start_urls가 리스트 형태로 각 상세페이지의 주소들을 가지고 있습니다.
    
    
    def parse(self, response):
        # response 받아온 데이터를 json으로 변환 후
        json_response = json.loads(response.body)
        # html 코드가 str형태로 들어있는 value를 찾아 BeautifulSoup으로 파싱합니다.
        data = json_response['data']['template']       
        dom = BeautifulSoup(data, "html.parser")
        
        # 아래에 중복되는 코드를 변수로 뺏습니다.
        root = dom.select('#company-list > div.company.item > div.content')
        positions = dom.select('#company-list > div.company.item > div.content > div.company-jobs-detail')

        for i in range(len(root)):
            len_of_positions = len(positions[i].select('div:nth-child(1) > a.nowrap')) 
            
            for j in range(len_of_positions):
                link = "https://www.rocketpunch.com" + positions[i].select('div:nth-child(1) > a.nowrap')[j].get('href') 
                response = requests.get(link)
                dom_for_skills = BeautifulSoup(response.text,"html.parser")    
                
                item = JobHunterItem()
                item['date'] = datetime.datetime.now()

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