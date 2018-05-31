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


class IqiyiTVItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
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
    region = scrapy.Field()
    positive = scrapy.Field()
    sex = scrapy.Field()
    ages = scrapy.Field()
    subtitle = scrapy.Field()
    numTotal = scrapy.Field()


class IqiyiCartoonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    # directors = scrapy.Field()
    Actors = scrapy.Field()
    period = scrapy.Field()
    description = scrapy.Field()
    pay = scrapy.Field()
    score = scrapy.Field()
    total = scrapy.Field()
    # tags = scrapy.Field()
    type = scrapy.Field()
    region = scrapy.Field()
    version = scrapy.Field()
    sex = scrapy.Field()
    ages = scrapy.Field()
    subtitle = scrapy.Field()
    inLanguage = scrapy.Field()
    number = scrapy.Field()

class IqiyiChildItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    # directors = scrapy.Field()
    Actors = scrapy.Field()
    period = scrapy.Field()
    description = scrapy.Field()
    pay = scrapy.Field()
    score = scrapy.Field()
    total = scrapy.Field()
    # tags = scrapy.Field()
    type = scrapy.Field()
    region = scrapy.Field()
    version = scrapy.Field()
    sex = scrapy.Field()
    ages = scrapy.Field()
    subtitle = scrapy.Field()
    inLanguage = scrapy.Field()
    number = scrapy.Field()

class IqiyiShowItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    # directors = scrapy.Field()
    Actors = scrapy.Field()
    period = scrapy.Field()
    description = scrapy.Field()
    pay = scrapy.Field()
    score = scrapy.Field()
    total = scrapy.Field()
    # tags = scrapy.Field()
    type = scrapy.Field()
    region = scrapy.Field()
    version = scrapy.Field()
    sex = scrapy.Field()
    ages = scrapy.Field()
    subtitle = scrapy.Field()
    inLanguage = scrapy.Field()
    number = scrapy.Field()
