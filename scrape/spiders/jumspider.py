from scrape.items import ScrapeItem
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from telebot import TeleBot

bot_token = "817904118:AAHgjvmKTrFqu3ya-u1Bt4IklckAoIGMnLk"
bot = TeleBot(bot_token)

class JumSpider(scrapy.Spider):
    name = "bonus"
    url_matcher = re.compile(r'^https:\/\/www\.jumia\.com\.ng\/(?!$)')
    crawled_ids = set()
    tag_extractor = re.compile(r'alt="([^"]*)"')
    src_extractor = re.compile(r'data-src="([^"]*)"')
    price_extractor = re.compile(r'data-price="([^"]*)"')
    tit_extractor = re.compile(r'title="([^"]*)"')

    def start_requests(self):
        url = "https://www.jumia.com.ng"
        yield scrapy.Request(url,self.parse)

    def parse(self, response):
        body = Selector(text=response.body)
        images = body.css('div.thumbs img.lazy').extract()
        details = body.css('div.details-wrapper span [data-price]').extract()
        try:
            price = min(int(JumSpider.price_extractor.findall(detail)[0]) for detail in details)
        except:
            price = 2501
        
        if price>=1200:
            # print(F'PRICE: {price}')
            # img_url = JumSpider.src_extractor.findall(images[0])[0]
            tag = JumSpider.tag_extractor.findall(images[0])[0]
            if re.search(r'(playstation)|(play station)|(PS4)|(PS 4)',tag,re.I):
                bot.send_message(770607717,F'''
                title: {tag}
                link: {response.url}
                price: {price}
                ''')
                yield ScrapeItem(title = tag, file_urls=[response.url],price=price)
            bot.send_message(770607717,F'''
                title: {tag}
                link: {response.url}
                price: {price}
                ''')
            exit()
            # print(F'image: {img_url}')
            # print(F'tag: {tag}')
            # yield ScrapeItem(title = tag, file_urls=[response.url],price=price)                

        link_extractor = LinkExtractor(allow=JumSpider.url_matcher)
        next_links = [link.url for link in link_extractor.extract_links(response) if not self.is_extracted(link.url)]

        for link in next_links:
            yield scrapy.Request(link,self.parse)

    def is_extracted(self,url):
        id = url.split('/')[-1]
        try:
            id = id[:id.rindex('html')+4]
        except:
            pass
        if id not in JumSpider.crawled_ids:
            JumSpider.crawled_ids.add(id)
            return False
        return True