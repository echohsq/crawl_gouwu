import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyuniversal.items import NewsItem

class NewsSpider(CrawlSpider):
    name = 'news'
    allowed_domains = ['tech.china.com']
    start_urls = ['http://tech.china.com/articles/']

    rules = (
        Rule(LinkExtractor(allow=r'article/.*.html', restrict_xpaths='//div[@id="rank-defList"]//div[@class="item_con"]'), callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="pages"]//a[contains(., "下一页")]'))
    )

    def parse_item(self, response):
        item = NewsItem()
        loader = ChinaLoader(item=NewsItem(), response=response)
        loader.add_xpath('title', '//h1[@id="chan_newsTitle"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('text', '//div[@id="chan_newsDetail"]//text()')
        loader.add_xpath('datetime', '//div[@id="chan_newsInfo"]/text()', re='(d+-d+-d+sd+:d+:d+)')
        loader.add_xpath('source', '//div[@id="chan_newsInfo"]/text()', re=' 来源：(.*)')
        loader.add_value('website', ' 中华网 ')
        yield loader.load_item()
 
