# -*- coding: utf-8 -*-
import random
import re
import sys
import time

import redis
import scrapy

from iqiyiCrawler.items import IqiyicrawlerItem

reload(sys)
sys.setdefaultencoding('utf-8')
conn = redis.Redis(host="10.4.255.129", port=6379, db=0)
# conn = redis.Redis(host="localhost", port=6379, db=0)


class IqiyiSpider(scrapy.Spider):
    name = 'iqiyi'
    # allowed_domains = ['iqiyi.com']
    urls = [
        "http://mixer.video.iqiyi.com/jp/recommend/videos?referenceId=732915800&albumId=732915800&channelId=1&cookieId=496db0c22d9a27a875d612af58b6e7c6&area=bee&size=48&type=video"]
    url = "http://mixer.video.iqiyi.com/jp/recommend/videos?referenceId={albumId}&albumId={albumId}&channelId=1&cookieId=496db0c22d9a27a875d612af58b6e7c6&area=bee&size=48&type=video"
    movie_url = "http://mixer.video.iqiyi.com/jp/mixin/videos/"
    tag_url = "http://qiqu.iqiyi.com/apis/video/tags/get?entity_id={albumId}&limit=10&area=azalea"
    gender_url = "https://uaa.if.iqiyi.com/video_index/v2/get_user_profile?album_id={albumId}"

    # albumId = ""
    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse_first)
            break

    def parse_first(self, response):
        # print("--------------------------------------------")
        result = response.text
        albumIds = re.findall('"albumId":(.*?),"videoType"', result)
        for albumId in albumIds:
            if conn.sadd("Iqiyi:movie", albumId) == 1:
                url = self.url.format(albumId=albumId)
                yield scrapy.Request(url=url, meta={"albumId": albumId}, callback=self.parse_index)

    def parse_index(self, response):
        albumId = response.meta["albumId"]
        gender_url = self.gender_url.format(albumId=albumId)
        yield scrapy.Request(url=gender_url, meta={"albumId": albumId}, callback=self.parse_gender)

    def parse_gender(self, response):
        albumId = response.meta["albumId"]
        tag_url = self.tag_url.format(albumId=albumId)
        genders = re.findall('"gender":\[(.*?)],', response.text)
        ages = re.findall('"age":\[(.*?)],', response.text)
        gender = ""
        age = ""
        for g in genders:
            gender = g
        for a in ages:
            age = a
        data = {"gender": gender, "age": age, "albumId": albumId}
        yield scrapy.Request(url=tag_url, meta={"data": data}, callback=self.parse_tag)

    def parse_tag(self, response):
        albumId = response.meta["data"].get("albumId")
        movie_url = self.movie_url + albumId + "?select=user,credit,focus,star,cast,gender"
        gender = response.meta["data"].get("gender")
        age = response.meta["data"].get("age")
        tags = re.findall('"tag":"(.*?)",', response.text)
        tag = ""
        for t in tags:
            tag = tag + "/" + t
        data = {"tag": tag, "gender": gender, "age": age, "albumId": albumId}
        yield scrapy.Request(url=movie_url, meta={"data": data}, callback=self.parse_all)

    def parse_all(self, response):
        result = response.text.strip("var tvInfoJs=")
        tags = response.meta["data"].get("tag").strip("/")  # 电影标签
        sex = response.meta["data"].get("gender")
        ages = response.meta["data"].get("age")
        albumId = response.meta["data"].get("albumId")
        name = re.findall('"name":"(.*?)",', result)  # 电影名
        type = ""
        spec = ""
        for a in name:
            if a in "喜剧、悲剧、爱情、动作、枪战、犯罪、惊悚、恐怖、悬疑、动画、家庭、奇幻、魔幻、科幻、战争、青春":
                type = type + a + "/"
            if a in "巨制、院线、独播、网络大电影、经典、口碑佳片、杜比、电影节目、4K、原声、粤语" and a != "电影":
                spec = spec + a + "/"
        # albumId = re.findall('"albumId":(.*?),', result)  # 电影ID
        title = re.findall('"title":"(.*?)",', result)  # 判断是否收费
        description = re.findall('"description":"(.*?)",', result)  # 简介
        if len(description) != 0:
            description = description[0]
        duration = re.findall('"duration":(.*?),', result)  # 片长 单位 秒
        if len(duration) != 0:
            duration = duration[0]
        upCount = re.findall('"upCount":(.*?),', result)  # 点赞数
        downCount = re.findall('"downCount":(.*?),', result)  # 踩数
        period = re.findall('"period":"(.*?)",', result)  # 发行时间
        if len(period) != 0:
            period = period[0]
        directors = re.findall('"directors":\["(.*?)"],', result)  # 导演
        if len(directors) != 0:
            directors = directors[0]
        mainActors = re.findall('"mainActors":\s*\[{(.*?)}],', result)
        positive = "正片"
        ma = ""
        mas = []
        if not len(mainActors):
            for mainActor in mainActors:
                mas = re.findall('"name":"(.*?)",', mainActor)
            if mas:
                for i in range(len(mas)):
                    ma = ma + mas[i] + "/"
        Actors = ma  # 主演
        score = re.findall('"score":(.*?),', result)  # 评分
        if len(directors) != 0:
            score = score[0]
        starTotal = re.findall('"starTotal":(.*?),', result)
        if len(directors) != 0:
            starTotal = starTotal[0]
        titles = ""
        pay = ""
        for t in title:
            titles = titles + "," + t
        if "电影" in titles:
            if "VIP会员" in titles:
                pay = "是"
            else:
                pay = "否"
            item = IqiyicrawlerItem()
            item['albumId'] = albumId
            item['name'] = name[0]
            item['directors'] = directors
            item['Actors'] = Actors
            item['period'] = period
            item['description'] = description
            item['pay'] = pay
            item['score'] = score
            item['starTotal'] = starTotal
            item['tags'] = tags
            item['type'] = type.strip("/")
            item['spec'] = spec.strip("/")
            item['positive'] = positive
            item['sex'] = sex
            item['ages'] = ages
            item['duration'] = duration
            yield item
            time.sleep(round(random.uniform(4, 10), 2))
            # print(self.url.format(albumId=albumId))
            yield scrapy.Request(self.url.format(albumId=albumId), callback=self.parse_first, dont_filter=True)
