# -*- coding: utf-8 -*-
import scrapy


class ComputersSpider(scrapy.Spider):
    name = 'computers'
    allowed_domains = ['jumia.ug/computing/']
    start_urls = ['https://jumia.ug/computing/']

    def parse(self, response):
        products = response.xpath('//*[@class="sku -gallery"]')
        for product in products:
            # Use the . for custom selectors 
            pdt_title = product.xpath('.//*[@class="title"]/span[@class="name"]/text()').extract()
            pdt_img_link = product.xpath('.//a/div[@class="image-wrapper default-state"]/img/@data-src').extract()
            pdt_current_px = product.xpath('.//*[@class="price "]/span[2]/text()').extract()
            pdt_old_px = product.xpath('.//*[@class="price -old "]/span[2]/text()').extract()
            pdt_discount = product.xpath('.//*[@class="sale-flag-percent"]/text()').extract()
            pdt_link = product.xpath('.//*[@class="link"]/@href').extract()
            # item_link = response.xpath('//*[@class="sku -gallery"]/a/@href')

            yield{
             'TITLE': pdt_title,
             'IMG_LINK': pdt_img_link,
             'ITEM_LINK': pdt_link,
             'CURRENT PRICE': pdt_current_px,
             'OLD PRICE': pdt_old_px, 
             'DISCOUNT': pdt_discount}
            
        next_page_url = response.xpath('//*[@title="Next"]/@href').extract_first()
        abs_url = response.urljoin(next_page_url)
        yield scrapy.Request(abs_url, dont_filter=True)
