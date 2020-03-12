# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EplCrawlerItem(scrapy.Item):
    club_name = scrapy.Field()
    position = scrapy.Field()
    player = scrapy.Field()
    won = scrapy.Field()
    drawn = scrapy.Field()
    lost = scrapy.Field()
    gf = scrapy.Field()
    ga = scrapy.Field()
    gd = scrapy.Field()
    points = scrapy.Field()