# -*- coding: utf-8 -*-
import scrapy
from myproject.items import MyprojectItem


class FiddingSpider(scrapy.Spider):
    name = 'fidding'
    # allowed_domains = ['fidding.com']
    start_urls = [
        'http://fidding.me/'
    ]

    def parse(self, response):
        for sel in response.xpath('//article'):
            item = MyprojectItem()
            item['title'] = sel.xpath('h1/a/text()').extract()
            item['link'] = sel.xpath('h1/a/@href').extract()
            yield item

        # 下一页
        next_uri = response.xpath('//li[@class="next"]/a/@href').extract()
        if len(next_uri):
            # 修改url地址
            # 例如: http://fidding.me?page=2 => http://fidding.me/page?=2
            uri = next_uri[0]
            uri = uri[:17] + '/' + uri[17:]
            yield scrapy.Request(
                uri,
                method='GET',
                callback=self.parse
            )
