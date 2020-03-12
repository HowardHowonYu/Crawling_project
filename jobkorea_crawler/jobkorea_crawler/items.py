# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobkoreaCrawlerItem(scrapy.Item):

    company_name = scrapy.Field()
    deadline = scrapy.Field()
    business  = scrapy.Field()
    link = scrapy.Field()
    position = scrapy.Field()
    job_condition = scrapy.Field()
    keyword = scrapy.Field()
