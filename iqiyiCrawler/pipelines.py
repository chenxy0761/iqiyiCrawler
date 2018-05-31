# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from iqiyiCrawler.con_sql import Dba
from iqiyiCrawler.items import IqiyicrawlerItem, IqiyiTVItem, IqiyiCartoonItem, IqiyiChildItem, IqiyiShowItem


class IqiyicrawlerPipeline(object):
    def __init__(self):
        self.ora = Dba()
        self.Movie_Sql = """
                           INSERT INTO douban.iqiyi_movie(albumId, name, directors, Actors, period, description, pay, score, starTotal, tags, type, spec, positive, sex, ages, duration) 
                           VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');

                        """
        self.Tv_Sql = """
                           INSERT INTO douban.iqiyi_tv(url, name, directors, Actors, period, description, pay, score, starTotal, tags, type, spec, positive, sex, ages, subtitle, numTotal) 
                           VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');

                        """
        self.cartoon_Sql = """
                           INSERT INTO douban.iqiyi_cartoon(url, name, Actors, period, description, pay, score, total, type, region, sex, ages, subtitle, number, version, inLanguage) 
                           VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');

                        """
        self.child_Sql = """
                           INSERT INTO douban.iqiyi_child(url, name, Actors, period, description, pay, score, total, type, region, sex, ages, subtitle, number, version, inLanguage) 
                           VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');

                        """
        self.show_Sql = """
                           INSERT INTO douban.iqiyi_show(url, name, Actors, period, description, pay, score, total, type, region, sex, ages, subtitle, number, version, inLanguage) 
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

        if isinstance(item, IqiyiTVItem):
            sql = self.Tv_Sql % (
                item['url'],
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
                item['region'],
                item['positive'],
                item['sex'],
                item['ages'],
                item['subtitle'],
                item['numTotal']
            )
            # print(sql)
            try:
                self.ora.cux_sql_base(self.ora.connect(), sql)
            except Exception as e:
                print(str(e) + "  " + item['name'])

        if isinstance(item, IqiyiCartoonItem):
            sql = self.cartoon_Sql % (
                item['url'],
                item['name'],
                item['Actors'],
                item['period'],
                item['description'],
                item['pay'],
                item['score'],
                item['total'],
                item['type'],
                item['region'],
                item['sex'],
                item['ages'],
                item['subtitle'],
                item['number'],
                item['version'],
                item['inLanguage']
            )
            # print(sql)
            try:
                self.ora.cux_sql_base(self.ora.connect(), sql)
            except Exception as e:
                print(str(e) + "  " + item['name'])

        if isinstance(item, IqiyiChildItem):
            sql = self.child_Sql % (
                item['url'],
                item['name'],
                item['Actors'],
                item['period'],
                item['description'],
                item['pay'],
                item['score'],
                item['total'],
                item['type'],
                item['region'],
                item['sex'],
                item['ages'],
                item['subtitle'],
                item['number'],
                item['version'],
                item['inLanguage']
            )
            # print(sql)
            try:
                self.ora.cux_sql_base(self.ora.connect(), sql)
            except Exception as e:
                print(str(e) + "  " + item['name'])

        if isinstance(item, IqiyiShowItem):
            sql = self.show_Sql % (
                item['url'],
                item['name'],
                item['Actors'],
                item['period'],
                item['description'],
                item['pay'],
                item['score'],
                item['total'],
                item['type'],
                item['region'],
                item['sex'],
                item['ages'],
                item['subtitle'],
                item['number'],
                item['version'],
                item['inLanguage']
            )
            # print(sql)
            try:
                self.ora.cux_sql_base(self.ora.connect(), sql)
            except Exception as e:
                print(str(e) + "  " + item['name'])
