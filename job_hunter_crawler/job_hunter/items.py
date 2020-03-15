# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobHunterItem(scrapy.Item):
    date = scrapy.Field()
    company_name = scrapy.Field()
    business = scrapy.Field()
    position = scrapy.Field()
    link = scrapy.Field()
    salary_condition = scrapy.Field()
    deadline = scrapy.Field()
    keyword = scrapy.Field()
    location = scrapy.Field()