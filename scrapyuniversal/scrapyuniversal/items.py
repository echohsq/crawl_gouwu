# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field, Item


class NewsItem(Item):
    collection = table = 'tech_china'
    title = Field()
    url = Field()
    text = Field()
    datetime = Field()
    source = Field()
    website = Field()

