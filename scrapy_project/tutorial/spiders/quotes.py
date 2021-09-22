# scrapy genspider quotes 生成spider
from tutorial.items import QuoteItem
import scrapy


class QuotesSpider(scrapy.Spider):
    # 唯一，区分不同的spider
    name = 'quotes'
    # 允许爬取的域名，如果初始或后续请求链接不在域名下，请求链接将被过滤
    allowed_domains = ['quotes.toscrape.com']
    # spider启动时爬取的url列表
    start_urls = ['http://quotes.toscrape.com/']
    '''
    它是 Spider 的一个方法。默认情况下，被调用时 start_urls 里面的链接构成的请求完成下载执行后，返回的响应就会作为唯一的参数传递给这个函数。该方法负责解析返回的响应、提取数据或者进一步生成要处理的请求
    '''
    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item
        # 生成下一页链接, response有.css方法，.xpath方法，在使用css和xpath后可以使用re正则
        next = response.css('.pager .next a::attr(href)').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)
