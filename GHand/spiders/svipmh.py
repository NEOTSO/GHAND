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
    start_urls = ['https://m.svipmh.com/view/24220']
    # start_urls = ['https://m.svipmh.com/comic/621']

    rules = (
        Rule(LinkExtractor(allow=r'.+/view/\d*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # id = response.request.url.split('/')[-1].split('.')[0]
        title = response.xpath('//p[@class="view-fix-top-bar-title"]/text()').get()
        print('#'*80)
        print(title)
        image_urls = response.xpath('//div[@id="cp_img"]/img/@data-original').extract()
        next = response.xpath('//ul[@class="view-bottom-bar"]/li[last()]/a/@href').get()
        if (next != 'javascript:void(0)'):
            scrapy.Request(self.domain + next, callback=self.parse_item)
        yield SvipmhItem(title=title, image_urls=image_urls)