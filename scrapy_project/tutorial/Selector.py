# Scrapy内置数据提取方法 Selector 
from scrapy import Selector
body = '<html><head><title>Hello World</title></head><body></body></html>'
selector = Selector(text=body)
title = selector.xpath('//title/text()').extract_first()
print(title)