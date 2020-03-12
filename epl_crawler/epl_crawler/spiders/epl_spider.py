import scrapy
import time
from scrapy.selector import Selector
from selenium import webdriver

from epl_crawler.items import EplCrawlerItem

class EPLSpider(scrapy.Spider):
    name = "PremierLeague"
    allowed_domains = ['https://www.premierleague.com']
    start_urls = ['https://www.premierleague.com/tables?co=1&se=210&ha=-1']
    
    
    
    def __init__(self):
        # 기존 Spider 클래스의 생성자를 초기화 해준다.
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome('../chromedriver')
        
        
        
    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(10)
        
        html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        selector = Selector(text=html)
        rows = selector.xpath('//*[@id="mainContent"]/div[2]/div[1]/div[4]/div/div/div/table/tbody/tr[not(@class="expandable")]')
        
        for row in rows:
            item = EplCrawlerItem()
            item['club_name'] = row.xpath('./td[3]/a/span[2]/text()')[0].extract()
            item['position'] = row.xpath('./td[2]/span[1]/text()')[0].extract()
            item['player'] = row.xpath('./td[4]/text()')[0].extract()         
            item['won'] = row.xpath('./td[5]/text()')[0].extract()
            item['drawn'] = row.xpath('./td[6]/text()')[0].extract()
            item['lost'] = row.xpath('./td[7]/text()')[0].extract()
            item['gf'] = row.xpath('./td[8]/text()')[0].extract()
            item['ga'] = row.xpath('./td[9]/text()')[0].extract()
            item['gd'] = row.xpath('./td[10]/text()')[0].extract()            
            item['points'] = row.xpath('./td[11]/text()')[0].extract()
            yield item