import scrapy
from ..items import CommitSpiderItem
from time import strftime, gmtime
import pandas as pd
global count
import argparse
import os

class CommitSpider(scrapy.Spider):
    name = 'commit'
    allowed_domains = ['github.com']

    def __init__(self, *args, **kwargs):
        super(CommitSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]
    # 解析一级页面的parse函数
    def parse(self, response):
        item = CommitSpiderItem()
        url = str(response.request.url)
        project_url = response.xpath('//a[@data-pjax="#js-repo-pjax-container"]/@href').extract()
        commit_title = response.xpath('//p[@class="commit-title"]/text()').extract()
        commit_text = response.xpath('//div[@class="commit-desc"]/pre/text()').extract()
        time_space = response.xpath('//relative-time[@class="no-wrap"]/text()').extract()
        user_nickname = response.xpath('//a[@class="commit-author user-mention"]/text()').extract()
        item['commit_href'] = url
        item['project_url'] = 'https://github.com' + str(project_url[0])
        if commit_title:
            item['commit_title'] = commit_title[0]
        else:
            item['commit_title'] = ' '
        if commit_text:
            item['commit_text'] = commit_text[0]
        else:
            item['commit_text'] = ' '
        if time_space:
            item['time_space'] = time_space[0]
        else:
            item['time_space'] = ' '
        item['timestamp'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        if user_nickname:
            item['user_nickname'] = user_nickname[0]
        else:
            user_nickname2 = response.xpath('//span[@class="commit-author user-mention"]/text()').extract()
            if user_nickname2:
                item['user_nickname'] = user_nickname2[0]
            else:
                item['user_nickname'] = ' '
        # 提取链接并发给调度器入队列
        user_link = 'https://github.com/' + str(str(item['user_nickname']).replace(' ', ''))
        yield scrapy.Request(
            url = user_link,
            # meta参数: 传递item对象到下一个解析函数
            meta = {'item':item},
            callback = self.parse_two_html
        )

    # 解析二级页面函数(圈名 章节数 章节名 链接)
    def parse_two_html(self,response):
        # 基准xpath
        item = response.meta['item']
        user_work_for = response.xpath('//span[@class="p-org"]/div/text()').extract()
        user_organization = response.xpath('//div[@class = "border-top color-border-secondary pt-3 mt-3 clearfix hide-sm hide-md"]/a/@href').extract()
        if user_work_for:
            item['user_work_for'] = user_work_for[0]
        else:
            item['user_work_for'] = ' '
        if user_organization:
            item['user_organization'] = user_organization[0]
        else:
            item['user_organization'] = ' '
        yield item
