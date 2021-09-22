# -*- coding: utf-8 -*-
from urllib.parse import urlencode
import scrapy
from scrapy import Request
import json
from tutorial.items import ImageItem


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']

    def start_requests(self):
        data = {'ch': 'photography', 'listtype': 'new'}
        base_url = 'https://image.so.com/zjl?'
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            data['sn'] = page * 3
            params = urlencode(data)
            url = base_url + params
            yield Request(url, self.parse, meta={'proxy': 'http://10.22.98.21:8080'})

    def parse(self, response, **kwargs):
        result = json.loads(response.text)
        for image in result.get('list'):
            item = ImageItem()
            item['id'] = image.get('id')
            item['url'] = image.get('qhimg_url')
            item['title'] = image.get('title')
            item['thumb'] = image.get('qhimg_thumb')
            print('item', item)
            yield item
