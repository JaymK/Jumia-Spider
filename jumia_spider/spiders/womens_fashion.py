# -*- coding: utf-8 -*-
import scrapy


class WomensFashionSpider(scrapy.Spider):
    name = 'womens_fashion'
    allowed_domains = ['jumia.ug/women-s-fashion/']
    start_urls = ['https://jumia.ug/women-s-fashion//']

    def parse(self, response):
        pass
