# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# class GhandPipeline(object):
#     def process_item(self, item, spider):
#         return item

from scrapy.exporters import JsonLinesItemExporter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.settings import Settings
from scrapy import Request

class GhandPipeline(object):
    def open_spider(self, spider):
        print('爬虫开始了...')
        self.fp = open('data.json', 'wb')
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
        
    def process_item(self, item, spider):
        print('xxxxxxxxxxxxx')
        print('-'*80)
        print(item['id'])
        print(item['title'])
        print(item['date'])
        print(item['content'])
        print('-'*80)
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.fp.close()
        print('爬虫结束了...')


class GhandImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print('piping....')
        print(item)
        for image_url in item['image_urls']:
            yield Request(image_url)
        # request_objs = super(GhandImagesPipeline, self).get_media_requests(item, info)
        # print('item:------')
        # print(item)
        # for request_obj in request_objs:
        #     request_obj.item = item
        # return request_objs

    # def file_path(self, request, response=None, info=None):
    #     path = super(GhandImagesPipeline, self).file_path(request, response, info)
    #     print('xxxx')
    #     print(request.item)
    #     return path

    def item_completed(self, results, item, info):
        image_paths=[x['path'] for ok,x in results if ok]
        if not image_paths:
            raise DropItem('图片未下载好 %s'%image_paths)
