# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapeItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()