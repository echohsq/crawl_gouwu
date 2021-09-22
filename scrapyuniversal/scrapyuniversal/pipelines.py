# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
from itemadapter import ItemAdapter
import pymysql

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
        self.db = pymysql.connect(host=self.mysql_uri, user=self.username, password=self.password, db=self.mysql_db, charset='utf8mb4')
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        name = item.table
        print('name', name)
        data = dict(item)
        cols = ", ".join('`{}`'.format(k) for k in data.keys())

        val_cols = ', '.join('%({})s'.format(k) for k in data.keys())

        sql = "insert into " + name + " (%s) values(%s)"
        res_sql = sql % (cols, val_cols)
        # print('sql', data)
        try:
            # 查重处理
            self.cursor.execute(
                "select * from " + name + " where url = %s",
                item['url'])
            # 是否有重复数据
            repetition = self.cursor.fetchone()

            # 重复
            if repetition:
                pass
            else:
                self.cursor.execute(res_sql, data)  # 将字典data传入
                self.db.commit()
        except Exception as error:
            logging.debug(error)
            self.db.rollback()
        return item

    def close_spider(self, spider):
        self.db.close()
