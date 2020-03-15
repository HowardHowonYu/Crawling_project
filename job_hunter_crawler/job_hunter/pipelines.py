# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import datetime
import logging
import MySQLdb.cursors
from scrapy.exceptions import DropItem
from job_hunter.items import JobHunterItem
 
 
class JobHunterPipeline(object):
    def __init__(self):
        # try:
            self.conn = MySQLdb.connect(user='root', passwd='dss', db='job_hunter', host='15.164.136.109', charset="utf8", use_unicode=True)
            #print("1")
            self.cursor = self.conn.cursor()
            #print("2")
        # except MySQLdb.Error, e:
        #     print "Error %d: %s" % (e.args[0], e.args[1])
        #     sys.exit(1)                
        # #log data to json file
 
 
    def process_item(self, item, spider):      
        # create record if doesn't exist.
        self.cursor.execute("select * from job_hunter where date = %s and company_name = %s and business = %s and position = %s and link = %s and salary_condition = %s and deadline = %s and keyword = %s and location = %s", (item['date'], item["company_name"].encode('utf-8'), item["business"].encode('utf-8'), item["position"].encode('utf-8'), item["link"].encode('utf-8'), item["salary_condition"].encode('utf-8'), item["deadline"].encode('utf-8'), item["keyword"].encode('utf-8'), item['location'].encode('utf-8')))
        result = self.cursor.fetchone()
        # print "select * from apt2u.apt where aptname = '%s' and link = 'http://www.apt2you.com/houseSaleDetailInfo.do?manageNo=%s' and company = '%s' and receiptdate = '%s' and result_date = '%s'" % (item['aptname'][0].encode('utf-8'), item['link'][0].encode('utf-8'), item['company'][0].encode('utf-8'), item['receiptdate'][0].encode('utf-8'), item['result_date'][0].encode('utf-8'))
 
        # if result:
        #     print("data already exist")    
        # else:
        #     try:
        self.cursor.execute("insert into job_hunter(date, company_name, business, position, link, salary_condition, deadline, keyword, location) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (item['date'], item["company_name"].encode('utf-8'), item["business"].encode('utf-8'), item["position"].encode('utf-8'), item["link"].encode('utf-8'), item["salary_condition"].encode('utf-8'), item["deadline"].encode('utf-8'), item["keyword"].encode('utf-8'), item['location'].encode('utf-8')))
        self.conn.commit()
    # except MySQLdb.Error, e:
            #     print "Error %d: %s" % (e.args[0], e.args[1])
        return item 








# # -*- coding: UTF-8 -*-

# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# from .mongodb import collection
# from sqlalchemy.orm import sessionmaker
# from .models import Channels, db_connect, create_channel_table
# from sqlalchemy.exc import SQLAlchemyError

# import time
# import json
# import requests


# class JobHunterPipeline(object):
    
#     def __init__(self):
#         # 변수선언은 여기서
#         self.webhook_url = "https://hooks.slack.com/services/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"
#         self.keyword = "데이터"

#                 #Initializes database connection and sessionmaker.
#         engine = db_connect()
#         create_channel_table(engine)
#         Session = sessionmaker(bind=engine)
#         self.session = Session()


    
#     def send_msg(self, msg):
#         payload = {
#             "channel" : "#구인공고",
#             "username" : "여기어때?",
#             "icon_emoji" : ":thumbsup:",
#             "text" : msg,
#         }
        
#         requests.post(self.webhook_url,json.dumps(payload))
#         time.sleep(1)
    
        
#     def process_item(self, item, spider):

#         record = Channels(date=item['date'],
#                              company_name=item['company_name'].encode('utf-8'),
#                              business=item['business'].encode('utf-8'),
#                              position=item['position'].encode('utf-8'),
#                              link=item['link'].encode('utf-8'),
#                              salary_condition = item['salary_condition'].encode('utf-8'),
#                              deadline = item['deadline'].encode('utf-8'),
#                              keyword = item['keyword'].encode('utf-8'),
#                              location = item['location'].encode('utf-8')                             
#                              )
#         self.session.add(record)
#         self.session.commit()



#         # for k,v in item.items():
#         #     item[k] = str(v.encode("utf-8"), 'utf-8')

       
#        # check if item with this title exists in DB
#         # item_exists = self.session.query(Channels).filter_by(position=item['position']).first()

#         # # if item exists in DB - we just update 'date' and 'subs' columns.
#         # if item_exists:
#         #     item_exists.position = item['position']
#         #     print('Item {} updated.'.format(item['position']))

#         # # if not - we insert new item to DB
#         # else:     
#         #     new_item = Channels(**item)
#         #     self.session.add(new_item)
#         #     print('New item {} added to DB.'.format(item['position']))

#         # new_item = Channels(**item)
#         # self.session.add(new_item)
#         # print('New item {} added to DB.'.format(item['position']))

#         # if self.keyword in item["position"]:
#         #     self.send_msg("회사명 : {} \n 직무 : {} \n 링크 : {}".format(item["company_name"],item["position"], item["link"]))
            
#         return item


#     # def close_spider(self, spider):
#     #     # We commit and save all items to DB when spider finished scraping.
#     #     try:
#     #         self.session.commit()
#     #     except SQLAlchemyError as e:
#     #         print(str(e))
#     #         self.session.rollback()
#     #         raise
#     #     finally:
#     #         self.session.close()

