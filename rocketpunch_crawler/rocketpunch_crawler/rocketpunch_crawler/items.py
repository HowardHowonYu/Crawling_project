# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RocketpunchCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    company = scrapy.Field()
    description = scrapy.Field()
    service = scrapy.Field()
    position = scrapy.Field()
    link = scrapy.Field()
    salary = scrapy.Field()
    deadline = scrapy.Field()
    pass
