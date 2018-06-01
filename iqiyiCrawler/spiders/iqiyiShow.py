# -*- coding: utf-8 -*-
import json
import re
import sys

import redis
import scrapy

from iqiyiCrawler.items import IqiyiTVItem, IqiyiShowItem

reload(sys)
sys.setdefaultencoding('utf-8')


conn = redis.Redis(host="10.4.255.129", port=6379, db=0)


class IqiyiSpider(scrapy.Spider):
    name = 'iqiyiShow'
    cache_urls = "http://cache.video.iqiyi.com/jp/vi/{tvid}/{vid}/"
    # http://mixer.video.iqiyi.com/jp/mixin/videos/1033851800
    urls = "http://mixer.video.iqiyi.com/jp/recommend/videos?referenceId={referenceId}&albumId={albumId}&channelId=6&cookieId=496db0c22d9a27a875d612af58b6e7c6&withRefer=false&area=bee&size=36&type=video&pru=&locale=&userId=&playPlatform=PC_QIYI&isSeriesDramaRcmd="
    url = ["http://www.iqiyi.com/v_19rrl7cb7o.html",
           "http://www.iqiyi.com/v_19rrebeqks.html",
           "http://www.iqiyi.com/v_19rrd8tezg.html",
           "http://www.iqiyi.com/v_19rr0lfu3s.html",
           "http://www.iqiyi.com/v_19rrddwae0.html"]
    jiming_url = "http://mixer.video.iqiyi.com/jp/mixin/videos/avlist?albumId={albumId}&size={size}&page=1"
    gender_url = "https://uaa.if.iqiyi.com/video_index/v2/get_user_profile?album_id={albumId}"
    # "https://uaa.if.iqiyi.com/video_index/v2/get_user_profile?album_id=203408601 203408601"
    tv_url = "http://mixer.video.iqiyi.com/jp/mixin/videos/{albumId}?select=user,credit,focus,star,cast,gender"

    def start_requests(self):
        for url in self.url:
            yield scrapy.Request(url=url, callback=self.parse_index)
        # for url in self.start_urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = response.meta["data"]
        result = response.text.strip("var tvInfoJs=")
        # print(result)
        jj = json.loads(result)
        # print(jj.get("albumQipuId"))
        data["keyword"] = jj.get("an")
        # print(jj.get("qiyiPlayStrategy"))
        data["tg"] = jj.get("tg")
        data["info"] = jj.get("info")
        data["d"] = jj.get("d")
        data["ma"] = jj.get("ma")
        # print(jj.get("nurl"))
        # print(jj.get("videoQipuId"))
        albumid = data.get("sid")
        # print(self.gender_url.format(albumId=albumid))
        yield scrapy.Request(url=self.gender_url.format(albumId=albumid), meta={"data": data},
                             callback=self.parse_gender, dont_filter=True)

    def parse_gender(self, response):
        data = response.meta["data"]
        albumid = data.get("albumid")
        sid = data.get("sid")
        tvid = data.get("tvid")
        result = json.loads(response.text)
        # print(albumid)
        gender = ""
        age = ""
        # print(result.get("data"))
        try:
            gender = result.get("data").get("details")[0].get(sid).get("gender")
        except:
            gender = ""
        try:
            age = result.get("data").get("details")[0].get(sid).get("age")
        except:
            pass
        data["gender"] = gender
        data["age"] = age
        yield scrapy.Request(url=self.tv_url.format(albumId=tvid), meta={"data": data}, callback=self.parse_score,
                             dont_filter=True, priority=2)

    def parse_score(self, response):
        data = response.meta["data"]
        result = json.loads(response.text.strip("var tvInfoJs="))
        score = result.get("score")
        playCount = result.get("playCount")
        data["score"] = score
        data["playCount"] = playCount
        item = IqiyiShowItem()
        item["url"] = data.get("url")
        item["name"] = data.get("keyword")
        item["directors"] = data.get("d")
        item["Actors"] = data.get("ma")
        item["period"] = data.get("time")
        item["description"] = data.get("info")
        item["pay"] = data.get("vip")
        item["score"] = score
        item["starTotal"] = playCount
        item["tags"] = data.get("tg")
        item["type"] = data.get("genres")
        item["region"] = data.get("region")
        item["positive"] = "正片"
        item["sex"] = data.get("gender")
        item["ages"] = data.get("age")
        item["subtitle"] = data.get("subtitle")
        item["numTotal"] = str(data.get("status"))
        # print(item["numTotal"])
        yield item
        # print(item)

    def parse_item(self, response):
        # print(response.meta["data"])
        albumid = response.meta["data"].get("albumid")
        data_page = response.meta["data"].get("page")
        data = response.meta["data"]
        # print(data)
        yield scrapy.Request(
            url=self.jiming_url.format(albumId=albumid, size=str(data_page * 30)),
            meta={"data": data}, callback=self.parse_num, dont_filter=True, priority=1)
        # print(response.text)
        result = response.text.strip("var tvInfoJs=")
        jj = json.loads(result)
        for tt in jj.get("mixinVideos"):
            url = tt.get("url")
            # print(tt.get("url"))
            # print(tt.get("description"))
            # print(tt.get("tvId"))
            # print(tt.get("albumId"))
            # print(tt.get("crumbList")[1].get("title"))
            # print(tt.get("crumbList")[2].get("title"))
            if conn.sadd("Iqiyi:show", url) == 1:
                yield scrapy.Request(url=url, callback=self.parse_index, dont_filter=True)

    def parse_index(self, response):
        sel = scrapy.Selector(response)
        # print(response.url)
        result = response.text
        # print(result)
        albumid = re.findall("param\['albumid']\s=\s(.*?);", result)
        tvid = re.findall("param\['tvid']\s=\s(.*?);", result)
        vid = re.findall("param\['vid']\s=\s(.*?);", result)
        sid = re.findall("sourceId:(.*?),", result)
        status = sel.xpath('//div[@class="playList-update-tip "]/p/text()').extract_first(default="")
        data_page = sel.xpath('//div[@data-tab-page="body"]').extract()
        site = sel.xpath('//div[@class="mod-juji-album-vip"]').extract()
        # print(site)
        vip = "免费"
        if len(site) == 0:
            vip = "收费"
        region = re.findall('rseat="707181_region">(.*?)</a>', result)
        genres = re.findall('rseat="707181_genres">(.*?)</a>', result)
        time = re.findall('rseat="707181_time"\starget="_blank">(.*?)</a>', result)
        if len(region) == 0:
            region = ["None"]
        if len(genres) == 0:
            genres = ["None"]
        if len(time) == 0:
            time = ["None"]
        if len(albumid) == 0:
            yield scrapy.Request(url=response.url, callback=self.parse_index, dont_filter=True)
        else:
            # print(region[0])  # 地区
            # print(genres[0])  # 种类
            # print(time[0])  # 年代
            # print(len(data_page))  # 页数
            data = {"url": response.url, "status": status, "sid": str(sid[0]).strip("\""), "vip": str(vip),
                    "vid": vid[0].strip("\""),
                    "tvid": tvid[0].strip("\""),
                    "albumid": albumid[0].strip("\""),
                    "region": region[0].strip("\""),
                    "genres": genres[0].strip("\""),
                    "time": time[0].strip("\""),
                    "page": len(data_page)}
            # yield scrapy.Request(
            #     url=self.jiming_url.format(albumId=str(albumid[0]).strip("\""), size=str(len(data_page) * 30)),
            #     callback=self.parse_num)
            yield scrapy.Request(
                url=self.urls.format(referenceId=str(tvid[0]).strip("\""), albumId=str(albumid[0]).strip("\"")),
                meta={"data": data}, callback=self.parse_item, dont_filter=True)

    def parse_num(self, response):
        result = response.text.strip("var tvInfoJs=")
        # print(result)
        jj = json.loads(result)
        data = response.meta["data"]
        subtitle = ""
        for i in range(len(jj.get("mixinVideos"))):
            subtitle = subtitle + "第" + str(i + 1) + "集:" + jj.get("mixinVideos")[i].get("subtitle") + ";"
        data["subtitle"] = subtitle
        tvid = response.meta["data"].get("tvid")
        vid = response.meta["data"].get("vid")
        # print(self.cache_urls.format(tvid=tvid, vid=vid))
        yield scrapy.Request(url=self.cache_urls.format(tvid=tvid, vid=vid), meta={"data": data},
                             callback=self.parse, dont_filter=True)
