# -*- coding: utf-8 -*-
import scrapy
from time import sleep
import random


class DealsSpider(scrapy.Spider):
    name = 'deals'
    allowed_domains = ['jumia.ug/deals-of-the-week/']
    start_urls = ['http://jumia.ug/deals-of-the-week/']

    def parse(self, response):
        products = response.xpath('//*[@class="sku -gallery -validate-size "]')
        for product in products:
            # Use the . for custom selectors 
            if product.xpath('.//*[@class="sale-flag-percent"]/text()'):

                pdt_title = product.xpath('.//*[@class="title"]/span[@class="name"]/text()').extract_first()
                pdt_img_link = product.xpath('.//a/div[@class="image-wrapper default-state"]/img/@data-src').extract_first()
                pdt_current_px = product.xpath('.//*[@class="price"]/span[2]/text()').extract_first()
                pdt_old_px = product.xpath('.//*[@class="price -old "]/span[2]/text()').extract_first()
                pdt_discount = product.xpath('.//*[@class="sale-flag-percent"]/text()').extract_first()
                pdt_link = product.xpath('.//*[@class="link"]/@href').extract_first()

                item_link_name = pdt_link[21:]
                link_builder = f'http://c.jumia.io/?a=92064&c=554&p=r&E=kkYNyk2M4sk%3d&ckmrdr=https%3A%2F%2Fwww.jumia.ug%2F{item_link_name}&utm_source=cake&utm_medium=affiliation&utm_campaign=92064&utm_term='

                pdt_old_px = pdt_old_px.replace(',', '')
                pdt_current_px = pdt_current_px.replace(',', '')

                amnt_cut = int(pdt_old_px) - int(pdt_current_px)
                pdt_discount = int(pdt_discount.replace('%', '')) * -1
                pdt_title = pdt_title.lower()

                yield{
                'name': pdt_title,
                'img_link': pdt_img_link,
                'item_link': pdt_link,
                'item_link_name': item_link_name,
                'item_link_builder': link_builder,
                'current_price': pdt_current_px,
                'old_price': pdt_old_px, 
                'discount': pdt_discount,
                'saving': amnt_cut
                }
        

        sleep(random.randrange(1,5))
        next_page_url = response.xpath('//*[@title="Next"]/@href').extract_first()
        abs_url = response.urljoin(next_page_url)
        yield scrapy.Request(abs_url, dont_filter=True)