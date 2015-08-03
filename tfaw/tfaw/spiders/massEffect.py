# -*- coding: utf-8 -*-
import scrapy
from ..items import TfawItem


class MasseffectSpider(scrapy.Spider):
    name = "massEffect"
    allowed_domains = ["tfaw.com"]
    start_urls = [
    'http://www.tfaw.com/Companies/Dark-Horse/Series?series_name=Mass+Effect',
]

    def parse(self, response):
        for href in response.css('div a.boldlink::attr(href)'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        comic = TfawItem()
        comic['title'] = response.css('div.iconistan + b span.blackheader::text').extract()
        comic['price'] = response.css('span.blackheader ~ span.redheader::text').re('[$]\d+\.\d+')
        comic['upc'] = response.xpath('//html/body/table[1]/tr/td[4]/table[3]/tr/td/table/tr/td[contains(., "UPC:")]/following-sibling::td[1]/text()').extract()
        comic['url'] = response.url
        yield comic
