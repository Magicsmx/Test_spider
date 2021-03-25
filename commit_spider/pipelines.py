# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class CommitSpiderPipeline:
    def __init__(self, dbparams):
        self.connect = pymysql.connect(
            host=dbparams['host'],
            port=dbparams['port'],
            db=dbparams['db'],
            user=dbparams['user'],
            passwd=dbparams['passwd'],
            charset=dbparams['charset'],
            use_unicode=dbparams['use_unicode']
        )
        # 创建一个句柄
        self.cursor = self.connect.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        # 读取settings中的配置
        dbparams = dict(
            host=crawler.settings.get('MYSQL_HOST'),
            db=crawler.settings.get('MYSQL_DBNAME'),
            user=crawler.settings.get('MYSQL_USER'),
            passwd=crawler.settings.get('MYSQL_PASSWD'),
            port=crawler.settings.get('MYSQL_POR'),
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            use_unicode=False,
        )
        return cls(dbparams)

    def process_item(self, item, spider):
        if spider.name == 'commit':
            sql = 'insert ignore into commit_all(commit_href, project_url, commit_title, commit_text, user_nickname, user_work_for, user_organization, time_space, time_stamp) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            self.cursor.execute(sql, (item['commit_href'],item['project_url'],item['commit_title'],item['commit_text'],item['user_nickname'],item['user_work_for'],item['user_organization'],item['time_space'],item['timestamp']))
            self.connect.commit()
        return item

    def close_spider(self, spider):
        self.connect.close()

