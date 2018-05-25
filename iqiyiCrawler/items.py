# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IqiyicrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    albumId = scrapy.Field()
    name = scrapy.Field()
    directors = scrapy.Field()
    Actors = scrapy.Field()
    period = scrapy.Field()
    description = scrapy.Field()
    pay = scrapy.Field()
    score = scrapy.Field()
    starTotal = scrapy.Field()
    tags = scrapy.Field()
    type = scrapy.Field()
    spec = scrapy.Field()
    positive = scrapy.Field()
    sex = scrapy.Field()
    ages = scrapy.Field()
    duration = scrapy.Field()
