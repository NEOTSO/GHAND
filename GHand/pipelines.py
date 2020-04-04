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
from GHand.settings import IMAGES_STORE
from scrapy import Request
from scrapy.utils.misc import md5sum

import os

class GhandPipeline(object):
    def open_spider(self, spider):
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
        # for image_url in item['image_urls']:
        #     yield Request(image_url)
        request_objs = super(GhandImagesPipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        path = super(GhandImagesPipeline, self).file_path(request, response, info)
        # print(request.url)
        # print(request.item.get('images'))
        # print(request.item.get('image_urls').index(request.url))
        index = request.item.get('image_urls').index(request.url)
        images_store = IMAGES_STORE
        print('***===***')
        print(images_store)
        print(request.item.get('images')[index])
        # image_path = os.path.join(images_store, request.item.get('images')[index])
        image_path = request.item.get('images')[index]
        print(image_path)
        return image_path

    def check_gif(self, image):
            if image.format is None:
                return True

    def persist_gif(self, key, data, info):
        root, ext = os.path.splitext(key)
        absolute_path = self.store._get_filesystem_path(key)
        self.store._mkdir(os.path.dirname(absolute_path), info)
        f = open(absolute_path, 'wb')  # use 'b' to write binary data.
        f.write(data)

    def image_downloaded(self, response, request, info):
        checksum = None
        for path, image, buf in self.get_images(response, request, info):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            width, height = image.size
            if self.check_gif(image):
                self.persist_gif(path, response.body, info)
            else:
                self.store.persist_file(
                    path, buf, info,
                    meta={'width': width, 'height': height},
                    headers={'Content-Type': 'image/jpeg'})
        return checksum

    # def item_completed(self, results, item, info):
    #     image_paths=[x['path'] for ok,x in results if ok]
    #     if not image_paths:
    #         raise DropItem('图片未下载好 %s'%image_paths)
