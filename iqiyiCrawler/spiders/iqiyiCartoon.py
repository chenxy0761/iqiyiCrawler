# -*- coding: utf-8 -*-
import json
import re
import sys
import urllib

import redis
import scrapy

from iqiyiCrawler.items import IqiyiTVItem, IqiyiCartoonItem

reload(sys)
sys.setdefaultencoding('utf-8')

conn = redis.Redis(host="10.4.255.129", port=6379, db=0)


class IqiyiSpider(scrapy.Spider):
    name = 'iqiyiCT'
    cache_urls = "http://cache.video.iqiyi.com/jp/vi/{tvid}/{vid}/"
    # url = "http://www.iqiyi.com/a_19rrh8jj45.html"
    url = ["http://www.iqiyi.com/lib/m_212660514.html",
           "http://www.iqiyi.com/a_19rrhaj981.html",
           "http://www.iqiyi.com/a_19rrha64id.html",
           "http://www.iqiyi.com/a_19rrha648t.html",
           "http://www.iqiyi.com/a_19rrha1cyx.html",
           "http://www.iqiyi.com/lib/m_215659414.html",
           "http://www.iqiyi.com/lib/m_201544014.html"]
    gender_url = "https://uaa.if.iqiyi.com/video_index/v2/get_user_profile?album_id={albumId}"
    follow_url = "http://mixer.video.iqiyi.com/jp/recommend/videos?albumId={albumId}&channelId=4&area=panda&size=7&type=video"
    title_url = "http://cache.video.iqiyi.com/jp/avlist/{albumId}/{i}/50/"

    def start_requests(self):
        for url in self.url:
            yield scrapy.Request(url=url, callback=self.parse_index)
        # for url in self.start_urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        result = response.text.strip("var tvInfoJs=")
        # print(result)
        jj = json.loads(result)
        for urls in jj.get("mixinVideos"):
            url = urls.get("albumUrl")
            if conn.sadd("Iqiyi:cartoon", url) == 1:
                yield scrapy.Request(url=url, callback=self.parse_index)

    def parse_index(self, response):
        sel = scrapy.Selector(response)
        name = sel.xpath('//div[@class="result_detail"]//h1[@class="main_title"]/a/text()').extract_first(default="")
        albumId = sel.xpath(
            '//div[@class="result_detail"]//div[@id="movie-score-show"]/span/@data-score-tvid').extract_first(
            default="")
        datePublished = sel.xpath(
            '//div[@class="result_detail"]//h1[@class="main_title"]/span[@itemprop="datePublished"]//text()').extract_first(
            default="")
        contentLocation = sel.xpath(
            '//div[@class="result_detail"]//div[@itemprop="contentLocation"]//a/text()').extract_first()
        genres = sel.xpath('//div[@class="result_detail"]//div[@itemprop="genre"]//a/text()').extract()
        genre = ""
        if len(genres) != 0:
            for i in range(len(genres)):
                genre = genre + genres[i] + "/"
        inLanguage = sel.xpath('//div[@class="result_detail"]//div[@itemprop="inLanguage"]//a/text()').extract_first(
            default="")
        playCount = sel.xpath('//i[@id="widget-playcount"]/text()').extract_first(default="")
        description = sel.xpath(
            '//div[@class="result_detail"]//span[@data-moreorless="moreinfo"]/span/text()').extract_first(default="")
        vip = sel.xpath(
            '//img[@src="http://pic0.qiyipic.com/common/20171106/ac/1b/vip_100000_v_601_0_20.png"]').extract_first(
            default="")
        if vip == "":
            vip = "免费"
        else:
            vip = "收费"
        # print(response.text)
        actor = ""
        try:
            tt = str(response.text)[str(response.text).index("集数"):]
            total = tt[tt.index("rseat=\"jj-zjxx-text-0923\">") + 26:tt.index("</a>")].strip()
        except:
            total = ""
        try:
            tt = str(response.text)[str(response.text).index("版本"):]
            version = tt[tt.index("rseat=\"jj-zjxx-text-0923\">") + 26:tt.index("</a>")].strip()
        except:
            version = ""
        try:
            tt = str(response.text)[str(response.text).index("<em>配音"):]
            mas = tt[:tt.index("</em>")].strip()
            ma = re.findall('rseat="jj-zjxx-text-0923">(.*?)</a>', mas)
            for m in ma:
                actor = actor + m + "/"
        except Exception as e:
            actor = ""
        # print(actor)
        pages = sel.xpath('//div[@class="mod-album_tab_num"]/a/@data-avlist-page').extract()
        index = 1
        title = ""
        try:
            for i in range(len(pages)):
                titles = urllib.urlopen(self.title_url.format(i=str(i + 1), albumId=albumId)).read()
                jj = json.loads(titles.strip("var tvInfoJs=")).get("data").get("vlist")
                for j in jj:
                    title += "第" + str(index) + "集:" + j.get("vt") + ";"
                    index += 1
        # print(title)
        except:
            pass
        score_url = "http://score-video.iqiyi.com/beaver-api/get_sns_score?qipu_ids={albumId}&appid=21"
        text = urllib.urlopen(score_url.format(albumId=albumId)).read()
        score = ""
        try:
            score = json.loads(text).get("data")[0].get("sns_score")
        except:
            pass
        genders = json.loads(urllib.urlopen(self.gender_url.format(albumId=albumId)).read())
        gender = ""
        try:
            gender = genders.get("data").get("details")[0].get(albumId).get("gender")
        except:
            pass
        age = ""
        try:
            age = genders.get("data").get("details")[0].get(albumId).get("age")
        except:
            pass
        item = IqiyiCartoonItem()
        item["url"] = response.url
        item["name"] = name
        item["Actors"] = actor
        item["period"] = datePublished
        item["description"] = description
        item["pay"] = vip
        item["score"] = score
        item["total"] = playCount
        item["type"] = genre
        item["region"] = contentLocation
        item["version"] = version
        item["inLanguage"] = inLanguage
        item["sex"] = gender
        item["ages"] = age
        item["subtitle"] = title
        item["number"] = total
        yield item
        # print(item)
        # print(total)
        # print(version)
        # print(vip)
        # print(name)
        # print(datePublished)
        # print(genre)
        # print(inLanguage)
        # print(playCount)
        # print(description)
        yield scrapy.Request(
            url=self.follow_url.format(albumId=albumId), callback=self.parse)
