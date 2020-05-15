# svipmh.py
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from GHand.items import SvipmhItem

class SvipmhSpider(CrawlSpider):
    name = 'svipmh'
    domain = 'https://m.svipmh.com'
    allowed_domains = ['m.svipmh.com']
    start_urls = ['https://m.svipmh.com/comic/511']
    comic_name = ''

    rules = (
        Rule(LinkExtractor(allow=r'.+/comic/\d*'), callback='parse', follow=True),
        Rule(LinkExtractor(allow=r'.+/view/\d*'), callback='parse_item', follow=True),
    )

    def parse(self, response):
        print('7777')
        try:
            self.comic_name = response.xpath('//p[@class="detail-main-info-title"]/text()').get()
            charpter_urls = response.xpath('//ul[@id="detail-list-select"]/li/a/@href').extract()
            for charpter_url in charpter_urls:
                print(self.domain + charpter_url)
                yield scrapy.Request(self.domain + charpter_url, callback=self.parse_item)
        except Exception as e:
            print(e)

    def parse_item(self, response):
        title = response.xpath('//p[@class="view-fix-top-bar-title"]/text()').get()
        print('#'*80)
        print(title)
        image_urls = response.xpath('//div[@id="cp_img"]/img/@data-original').extract()
        yield SvipmhItem(name=self.comic_name, title=title, image_urls=image_urls)