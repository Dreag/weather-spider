# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeatherItem(scrapy.Item):
    # define the fields for your item here like:

    date = scrapy.Field()
    weather = scrapy.Field()
    tem_higher = scrapy.Field()
    tem_lower = scrapy.Field()
    city = scrapy.Field()

