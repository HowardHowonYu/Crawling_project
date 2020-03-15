# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# from .mongodb import collection
from sqlalchemy.orm import sessionmaker
from .models import Channels, db_connect, create_channel_table

import time
import json
import requests


class JobHunterPipeline(object):
    
    def __init__(self):
        # 변수선언은 여기서
        self.webhook_url = "https://hooks.slack.com/services/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"
        self.keyword = "데이터"

                #Initializes database connection and sessionmaker.
        engine = db_connect()
        create_channel_table(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()


    
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
        # check if item with this title exists in DB
        item_exists = self.session.query(Channels).filter_by(position=item['position']).first()
        # if item exists in DB - we just update 'date' and 'subs' columns.
        if item_exists:
            item_exists.position = item['position']
            print('Item {} updated.'.format(item['position']))
        # if not - we insert new item to DB
        else:     
            new_item = Channels(**item)
            self.session.add(new_item)
            print('New item {} added to DB.'.format(item['position']))

        if self.keyword in item["position"]:
                    self.send_msg("회사명 : {} \n 직무 : {} \n 링크 : {}".format(item["company_name"],item["position"], item["link"]))
            
        return item    


    def close_spider(self, spider):
        # We commit and save all items to DB when spider finished scraping.
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
