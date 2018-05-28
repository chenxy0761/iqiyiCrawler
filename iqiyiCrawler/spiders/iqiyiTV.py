# -*- coding: utf-8 -*-
import json
import re
import sys

import scrapy

reload(sys)
sys.setdefaultencoding('utf-8')


class IqiyiSpider(scrapy.Spider):
    name = 'iqiyiTV'
    start_urls = ["http://cache.video.iqiyi.com/jp/vi/638956700/6f7d21d9091f57c0e66ccb1df14867f4/"]
    # http://mixer.video.iqiyi.com/jp/mixin/videos/1033851800
    urls = "http://mixer.video.iqiyi.com/jp/recommend/videos?referenceId={referenceId}&albumId={albumId}&channelId=2&cookieId=496db0c22d9a27a875d612af58b6e7c6&withRefer=false&area=bee&size=36&type=video&pru=&locale=&userId=&playPlatform=PC_QIYI&isSeriesDramaRcmd="
    url = "http://www.iqiyi.com/v_19rrercswg.html"

    def start_requests(self):
        # yield scrapy.Request(url=self.url, callback=self.parse_index)
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        result = response.text.strip("var tvInfoJs=")
        # print(result)
        jj = json.loads(result)
        print(jj.get("albumQipuId"))
        print(jj.get("keyword"))
        print(jj.get("qiyiPlayStrategy"))
        print(jj.get("tg"))
        print(jj.get("info"))
        print(jj.get("d"))
        print(jj.get("ma"))
        print(jj.get("nurl"))
        print(jj.get("videoQipuId"))
        yield scrapy.Request(url=jj.get("nurl"), callback=self.parse_index)

    def parse_item(self, response):
        # print(response.text)
        result = response.text.strip("var tvInfoJs=")
        jj = json.loads(result)
        for tt in jj.get("mixinVideos"):
            url = tt.get("url")
            print(tt.get("url"))
            print(tt.get("description"))
            print(tt.get("tvId"))
            print(tt.get("albumId"))
            print(tt.get("crumbList")[1].get("title"))
            print(tt.get("crumbList")[2].get("title"))

        # yield scrapy.Request(url=url, callback=self.parse_index)

    def parse_index(self, response):
        sel = scrapy.Selector(response)
        result = response.text
        # print(result)
        albumid = re.findall("param\['albumid']\s=\s(.*?);", result)
        tvid = re.findall("param\['tvid']\s=\s(.*?);", result)
        vid = re.findall("param\['vid']\s=\s(.*?);", result)
        print(sel.xpath('//div[@class="playList-update-tip "]/p/text()')).extract_first(default="")
        titles = sel.xpath('//div[@data-tab-page="body"]/ul/li/a/@title').extract()
        region = re.findall('rseat="707181_region">(.*?)</a>', result)
        genres = re.findall('rseat="707181_genres">(.*?)</a>', result)
        time = re.findall('rseat="707181_time"\starget="_blank">(.*?)</a>', result)
        if len(titles) == 0:
            yield scrapy.Request(url=response.url, callback=self.parse_index, dont_filter=True)
        else:
            print(albumid, tvid, vid)
            print(region[0])
            print(genres[0])
            print(time[0])
            info = ""
            for i in range(len(titles)):
                info = info + "第" + str(i + 1) + "集:" + titles[i] + "\n"
            print(self.urls.format(referenceId=str(tvid[0]).strip("\""), albumId=str(albumid[0]).strip("\"")))
            yield scrapy.Request(
                url=self.urls.format(referenceId=str(tvid[0]).strip("\""), albumId=str(albumid[0]).strip("\"")),
                callback=self.parse_item, dont_filter=True)
