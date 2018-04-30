# -*- coding: utf-8 -*-
import scrapy
from jdspider import items
from scrapy import Request
import re
from jdspider import pipelines

class JdBookSpider(scrapy.Spider):
    name = 'jd_book'
    allowed_domains = ['search.jd.com']
    start_urls = 'https://search.jd.com/Search?keyword=%s&enc=utf-8&qrst=1&rt=1&stop=1&vt=2'

    def start_requests(self):
        keyWold = input('请输入书籍名称:')
        pipelines.topic['path'] = keyWold
        self.start_urls = str(self.start_urls) % keyWold
        yield Request(url=self.start_urls,callback=self.parse_urls,dont_filter=True)

    def parse_urls(self,response):
        pageNum = 1 # 设置停止测试
        # total = int(re.findall('page_count:"(\d+)"',response.text)[0])
        for i in range(pageNum):
            url = '%s&page=%s'%(self.start_urls,2*i+1)
            yield Request(url,callback=self.parse)

    def parse(self, response):
        li = response.css('ul.gl-warp.clearfix li.gl-item')
        book = items.books()
        for info in li:
            book['title'] = info.css('div.p-name').xpath('string(.//em)').extract_first()
            book['price'] = info.css('div.p-price i::text').extract_first()+"元"
            book['detail'] = info.css('i.promo-words::text').extract_first()
            if not book['detail']:
                book['detail']='无简介'
            book['author'] = info.css('span.p-bi-name a::text').extract_first()
            book['commitNum'] =info.css('div.p-commit a::text').extract_first()
            book['shopNum'] = info.css('div.p-shopnum a::text').extract_first()
            baseUrl ='//'+re.findall('="//(.*).jpg">',info.css('div.p-img img').extract_first())[0]+'.jpg'
            book['file_urls']= [response.urljoin(baseUrl)]
            yield book