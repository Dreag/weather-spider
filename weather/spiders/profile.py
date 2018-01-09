# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
from scrapy.selector import Selector
from weather.items import WeatherItem
import json


class ProfileSpider(scrapy.Spider):
    name = "profile"
    allowed_domains = ["www.weather.com.cn"]
    start_urls = ['http://www.weather.com.cn/']


    def start_requests(self):
        self.url = "http://www.weather.com.cn/weather/{code}.shtml"
        with open("weather_code.json", "r",encoding = 'utf-8') as f:
           self.weather_code = json.load(f)
        for self.key in self.weather_code:
            request = Request(url=self.url.format(code=self.key), callback=self.getweather)
            # 将城市天气代码传递到getweather函数中
            request.meta['code'] = self.key
            yield request

    def getweather(self, response):

        item = WeatherItem()
        selector = Selector(response)
        weather = selector.xpath('//div[@id="7d"]/ul[@class="t clearfix"]/li')
        for each in weather[:7]:
            item["city"] = self.weather_code[response.meta['code']]
            item["date"]= each.xpath('h1/text()').extract()[0]
            item["weather"] = each.xpath('p[@class="wea"]/text()').extract()[0]
            item["tem_higher"] = each.xpath('p[@class="tem"]/span/text()').extract()[0]
            item["tem_lower"] = each.xpath('p[@class="tem"]/i/text()').extract()[0]
            yield item
