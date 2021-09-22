# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
'''
要实现 Item Pipeline 很简单，只需要定义一个类并实现 process_item () 方法即可。启用 Item Pipeline 后，Item Pipeline 会自动调用这个方法。process_item () 方法必须返回包含数据的字典或 Item 对象，或者抛出 DropItem 异常. 在settings文件中启用
'''
from scrapy.exceptions import DropItem
import pymysql
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class TextPipeline(object):
    def __init__(self) -> None:
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing Text')


class MysqlPipeline(object):
    def __init__(self, mysql_uri, username, password, mysql_db) -> None:
        self.mysql_uri = mysql_uri
        self.username = username
        self.password = password
        self.mysql_db = mysql_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mysql_uri=crawler.settings.get('MYSQL_URI'),
                   username=crawler.settings.get('USERNAME'),
                   password=crawler.settings.get('PASSWORD'),
                   mysql_db=crawler.settings.get('MYSQL_DB')
                   )

    def open_spider(self, spider):
        self.db = pymysql.connect(host=self.mysql_uri, user=self.username, password=self.password, db=self.mysql_db)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        name = item.table
        data = dict(item)
        cols = ", ".join('`{}`'.format(k) for k in data.keys())

        val_cols = ', '.join('%({})s'.format(k) for k in data.keys())

        sql = "insert into " + name + " (%s) values(%s)"
        res_sql = sql % (cols, val_cols)
        try:
            self.cursor.execute(res_sql, data)  # 将字典data传入
            self.db.commit()
        except:
            self.db.rollback()
        return item

    def close_spider(self, spider):
        self.db.close()


class MongoPipeline(object):
    def __init__(self) -> None:
        pass

    @classmethod
    def from_crawler(cls, crawler):
        pass

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        pass

    def close_spider(self, spider):
        pass


# 继承Scrapy内置的ImagesPipeline
class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        url = request.url
        file_name = url.split('/')[-1]
        print('file_name', file_name)
        return file_name

    def item_completed(self, results, item, info):
        print('result', results)
        image_paths = [x['path'] for ok, x in results if ok]
        print('image_path', image_paths)
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item

    def get_media_requests(self, item, info):
        print('pic_url', item['url'])
        yield Request(url=item['url'])
