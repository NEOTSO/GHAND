# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from GHand.items import GhandItem
import re

class Hongxing1Spider(CrawlSpider):
    name = 'hongxing1'
    allowed_domains = ['hongxing1.com']
    start_urls = ['https://www.hongxing1.com/sheyingshequ/index.html']

    rules = (
        Rule(LinkExtractor(allow=r'.+/sheyingshequ/index_?\d*\.html'), follow=True),
        Rule(LinkExtractor(allow=r'.+/sheyingshequ/\d*\.html'), callback='parse_item', follow=True)
    )

    def filterStr(self, str):
        filtered = str.replace('\r', '').replace('\n', '').replace('\t', '').replace('<div class=\"nr_two_ad clearfix\"><div class=\"nr_two_ad1 fl\"><script src=\"/d/js/acmsd/thea9.js\"></script></div><div style=\"nr_two_ad2 fr\"><script src=\"/d/js/acmsd/thea10.js\"></script></div></div>', '').replace('<script src=\"/d/js/acmsd/thea9.js\"></script>', '')
        # filtered = re.sub(r'<div.+?>', '', filtered)
        # filtered = re.sub(r'</div>', '', filtered)
        # filtered = re.sub(r'<p.+?>', '', filtered)
        # filtered = re.sub(r'</p>', '', filtered)
        # filtered = re.sub(r'<span.+?>', '', filtered)
        # filtered = re.sub(r'</span>', '', filtered)
        # filtered = re.sub(r'<a.+?>', '', filtered)
        # filtered = re.sub(r'</a>', '', filtered)
        # filtered = re.sub(r'<strong.+?>', '', filtered)
        # filtered = re.sub(r'</strong>', '', filtered)
        filtered = re.sub(r'(?i)<(?!img|/img).*?>', '', filtered)
        filtered = filtered.replace('本文admin转自网络，由红星军事网(http://www.hongxing1.com/)整理编辑，版权归原作者所有。', '').replace('本文hongxing转自网络，由红星军事网(http://www.hongxing1.com/)整理编辑，版权归原作者所有。', '') .replace('红星军事网(http://www.hongxing1.com/)整理编辑，版权归原作者所有。', '')
        filtered = re.sub(r'<img.+src=".+/(.+\.(jpg|png|jpeg|gif))".+>?', r'\1', filtered)
        filtered = re.sub(r'qqmail_head\/(.+?)\/', r'\1', filtered)
        filtered = re.sub(r'<img.+src=".+?/p\.qlogo\.cn\/(.+)".+>?', r'\1', filtered)
        
        return filtered

    def parse_item(self, response):
        id = response.request.url.split('/')[-1].split('.')[0]
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        title = response.xpath('//div[@class="article"]/h1/text()').get()
        date = response.xpath('//div[@class="article"]/div[@class="wzxx"]/span/text()').get()
        content = self.filterStr(response.xpath('//div[@id="news"]').get())
        # print(content)
        yield GhandItem(id=id, title=title, date=date, content=content)
