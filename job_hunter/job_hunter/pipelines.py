# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .mongodb import collection

import time
import json
import requests


class JobHunterPipeline(object):
    
    def __init__(self):
        # 변수선언은 여기서
        self.webhook_url = "https://hooks.slack.com/services/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"
        self.keyword = "데이터"
    
    def send_msg(self, msg):
        payload = {
            "channel" : "#구인공고",
            "username" : "여기어때?",
            "icon_emoji" : ":thumbsup:",
            "text" : msg,
        }
        
        requests.post(self.webhook_url,json.dumps(payload))
        time.sleep(1)
    
        
    def process_item(self, item, spider):
        
        data = {
            "company_name": item["company_name"],
            "position": item["position"],
            "business": item["business"], 
            "deadline": item["deadline"],
            "link": item["link"],
            "keyword" : item["keyword"],
            "business" : item["business"],
            "salary_condition" : item["salary_condition"],
            
        }
    
        collection.insert(data)
        
        if self.keyword in item["position"]:
            self.send_msg("회사명 : {} \n 직무 : {} \n 링크 : {}".format(item["company_name"],item["position"], item["link"]))
            
            
        return item
    
