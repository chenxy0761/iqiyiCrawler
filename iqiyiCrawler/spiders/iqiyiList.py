# -*- coding: utf-8 -*-
import json
import re
import sys
import urllib

import redis
import scrapy

from iqiyiCrawler.items import IqiyiListItem

reload(sys)
sys.setdefaultencoding('utf-8')

# conn = redis.Redis(host="localhost", port=6379, db=0)
conn = redis.Redis(host="10.4.255.129", port=6379, db=0)


class IqiyiSpider(scrapy.Spider):
    name = 'iqiyiList'
    cache_urls = "http://cache.video.iqiyi.com/jp/vi/{tvid}/{vid}/"
    # url = "http://www.iqiyi.com/a_19rrh8jj45.html"
    url = "http://list.iqiyi.com/www/6/-------------11-{i}-1-iqiyi--.html"
    gender_url = "https://uaa.if.iqiyi.com/video_index/v2/get_user_profile?album_id={albumId}"
    follow_url = "http://mixer.video.iqiyi.com/jp/recommend/videos?albumId={albumId}&channelId=15&area=panda&size=7&type=video"
    # "http://mixer.video.iqiyi.com/jp/recommend/videos?albumId=202259301&channelId=15&area=panda&size=7&type=video&pru="
    title_url = "http://cache.video.iqiyi.com/jp/avlist/{albumId}/{i}/50/"

    def start_requests(self):
        for i in range(30):
            url = self.url.format(i=str(i + 1))
            yield scrapy.Request(url=url, callback=self.parse)
        # for url in self.start_urls:
        #     yield scrapy.Request(url=url, callback=self.parse)
        # "/html/body/div[3]/div/div/div[3]/div/ul/li[1]/div[2]/div[1]/p/a"

    def parse(self, response):
        sel = scrapy.Selector(response)
        url = sel.xpath('//div[@class="wrapper-piclist"]//li/div[2]/div[1]/p/a/@href').extract()
        for u in url:
            yield scrapy.Request(url=u, callback=self.parse_index)

    def parse_index(self, response):
        sel = scrapy.Selector(response)
        # //*[@id="block-BB"]/div/div/div[2]/div[2]/div/div[1]/p[1]/a
        name = sel.xpath('//div[@class="info-intro"]/h1/a[1]/@title').extract_first(default="")
        albumId = sel.xpath(
            '//div[@class="info-intro"]//div[@id="movie-score-show"]/span/@data-score-tvid').extract_first(
            default="")
        datePublished = sel.xpath(
            '//div[@class="info-intro"]//p[class="episodeIntro-update"]/span/text()').extract_first(
            default="")
        contentLocation = sel.xpath(
            '//div[@class="info-intro"]//p[@itemprop="contentLocation"]/a/text()').extract_first()
        genres = sel.xpath('//div[@class="info-intro"]//p[@itemprop="genre"]//a/text()').extract()
        genre = ""
        tv = sel.xpath('//div[@class="info-intro"]//p[@class="episodeIntro-lang"]/span/text()').extract_first(
            default="")
        if len(genres) != 0:
            for i in range(len(genres)):
                genre = genre + genres[i] + "/"
        inLanguage = sel.xpath('//div[@class="info-intro"]//p[@itemprop="inLanguage"]//a/text()').extract_first(
            default="")
        playCount = sel.xpath('//i[@id="widget-playcount"]/text()').extract_first(default="")
        description = sel.xpath(
            '//div[@class="info-intro"]//div[@data-moreorless="lessinfo"]/span/text()').extract_first(default="")
        vip = sel.xpath(
            '//img[@src="http://pic0.qiyipic.com/common/20171106/ac/1b/vip_100000_v_601_0_20.png"]').extract_first(
            default="")
        sourceId = ""
        try:
            sourceId = re.findall('sourceId:\s(.*?),', response.text)[0]
        except:
            pass
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
        item = IqiyiListItem()
        if sourceId != "":
            html = urllib.urlopen("http://cache.video.iqiyi.com/jp/sdvlst/6/" + sourceId + "/?categoryId=6").read()
            jj = json.loads(html.strip("var tvInfoJs="))
            for p in jj.get("data"):
                # print(p.get("mActors"), p.get("tvSbtitle"), p.get("tvYear"), p.get("score"), p.get("disCnt"))
                item["url"] = p.get("vUrl")
                item["name"] = name
                ma = ""
                for m in p.get("mActors"):
                    ma += m.get(m.keys()[0])+"/"
                item["Actors"] = ma
                item["period"] = datePublished.replace("'", "\"")
                item["description"] = description.replace("'", "\"")
                item["pay"] = vip
                item["score"] = score
                item["total"] = tv
                item["type"] = genre
                item["region"] = contentLocation
                item["version"] = p.get("tvYear").replace("'", "\"")
                item["inLanguage"] = inLanguage.replace("'", "\"")
                item["sex"] = gender
                item["ages"] = age
                item["subtitle"] = p.get("tvSbtitle").replace("'", "\"")
                item["number"] = str(p.get("disCnt"))
                if conn.sadd("Iqiyi:List", item["url"]) == 1:
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
        # # print(description)
        # yield scrapy.Request(
        #     url=self.follow_url.format(albumId=albumId), callback=self.parse)

    if __name__ == '__main__':
        [{u'214528505': u'\u6b27\u9633\u9756'}]
        st = "sssssssssssssssssssssss'sss's's''s'"
        print(st.replace("\'", "\""))
