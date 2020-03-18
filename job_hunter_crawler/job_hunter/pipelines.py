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
        self.conn = MySQLdb.connect(user='root', passwd='dss', db='job_hunter', host='15.164.136.109', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()
        
 
 
    def process_item(self, item, spider):      
        self.cursor.execute("INSERT INTO job_hunter (date, company_name, business, position, link, salary_condition, deadline, keyword, location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (item['date'], item["company_name"].encode('utf-8'), item["business"].encode('utf-8'), item["position"].encode('utf-8'), item["link"].encode('utf-8'), item["salary_condition"].encode('utf-8'), item["deadline"].encode('utf-8'), item["keyword"].encode('utf-8'), item['location'].encode('utf-8')))
        self.conn.commit()
    
        return item 





