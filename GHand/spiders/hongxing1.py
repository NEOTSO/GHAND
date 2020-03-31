# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from GHand.items import GhandItem

class Hongxing1Spider(CrawlSpider):
    name = 'hongxing1'
    allowed_domains = ['hongxing1.com']
    start_urls = ['https://www.hongxing1.com/sheyingshequ/index.html']

    rules = (
        Rule(LinkExtractor(allow=r'.+/sheyingshequ/index_?\d*\.html'), follow=True),
        Rule(LinkExtractor(allow=r'.+/sheyingshequ/\d*\.html'), callback='parse_item', follow=True)
    )

    def parse_item(self, response):
        id = response.request.url.split('/')[-1].split('.')[0]
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        title = response.xpath('//div[@class="article"]/h1/text()').get()
        date = response.xpath('//div[@class="article"]/div[@class="wzxx"]/span/text()').get()
        content = response.xpath('//div[@id="news"]').get()
        print(title)
        print(content)
        # return item
        yield GhandItem(id=id, title=title, date=date, content=content)
