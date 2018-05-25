# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from iqiyiCrawler.con_sql import Dba
from iqiyiCrawler.items import IqiyicrawlerItem


class IqiyicrawlerPipeline(object):
    def __init__(self):
        self.ora = Dba()
        self.Movie_Sql = """
                           INSERT INTO `douban`.`iqiyi_movie`(`albumId`, `name`, `directors`, `Actors`, `period`, `description`, `pay`, `score`, `starTotal`, `tags`, `type`, `spec`, `positive`, `sex`, `ages`, `duration`) 
                           VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');

                        """

    def process_item(self, item, spider):
        if isinstance(item, IqiyicrawlerItem):
            sql = self.Movie_Sql % (
                int(item['albumId']),
                item['name'],
                item['directors'],
                item['Actors'],
                item['period'],
                item['description'],
                item['pay'],
                item['score'],
                item['starTotal'],
                item['tags'],
                item['type'],
                item['spec'],
                item['positive'],
                item['sex'],
                item['ages'],
                item['duration']
            )
            # print(sql)
            try:
                self.ora.cux_sql_base(self.ora.connect(), sql)
            except Exception as e:
                print(str(e) + "  " + item['name'])
