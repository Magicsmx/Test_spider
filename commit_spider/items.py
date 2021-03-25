# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CommitSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # commit 链接
    commit_href = scrapy.Field()
    # 项目链接
    project_url = scrapy.Field()
    # commit 标题
    commit_title = scrapy.Field()
    # commit 描述
    commit_text = scrapy.Field()
    # 用户名
    user_nickname = scrapy.Field()
    # 用户公司
    user_work_for = scrapy.Field()
    # 用户组织
    user_organization = scrapy.Field()
    # 提交时间
    time_space = scrapy.Field()
    # 检测时间
    timestamp = scrapy.Field()
    pass
