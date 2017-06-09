import scrapy
import json
import re
import csv
import requests
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem

import pdb

class Kimbrells(scrapy.Spider):
    name = "kimbrells"

    domain = "https://www.kimbrells.com/"
    start_urls = ["https://www.kimbrells.com/AllShops"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('//li[@class="shops-item visible"]')
        for store_info in store_list:

            url = 'https://www.kimbrells.com%s' % store_info.xpath('.//a[@class="read-more"]/@href').extract_first()

            request = scrapy.Request(url=url, callback=self.parse_store)
            request.meta['lat'] = store_info.xpath('.//input/@data-latitude').extract()
            request.meta['lng'] = store_info.xpath('.//input/@data-longitude').extract()
            yield request

    def parse_store(self, response):
        store_info = response;
        item = ChainItem()

        item['store_number'] = ''
        item['store_name'] = store_info.xpath('.//div[@class="page-title"]/h1/text()').extract_first()
        item['address'] = store_info.xpath('.//div[@class="shop-full-description"]/p/text()').extract()[0].strip()
        item['address2'] = ''
        item['city'] = store_info.xpath('.//div[@class="shop-full-description"]/p/text()').extract()[1].split(',')[0].strip()
        item['state'] = "".join(store_info.xpath('.//div[@class="shop-full-description"]/p/text()').extract()[1].split(',')[1].strip().split(' ')[:-1])
        item['zip_code'] = store_info.xpath('.//div[@class="shop-full-description"]/p/text()').extract()[1].split(',')[1].strip().split(' ')[-1]
        item['country'] = 'United States'
        item['phone_number'] = store_info.xpath('.//div[@class="shop-full-description"]/p/a/text()').extract_first()
        item['latitude'] = response.meta['lat']
        item['longitude'] = response.meta['lng']
        item['store_hours'] = store_info.xpath('.//div[@class="shop-full-description"]/p/text()').extract()[2].strip()
        item['other_fields'] = ""
        item['coming_soon'] = "0"

        yield item

    def validate(self, value):
        if type(value) == "str":
            return value
        else:
            return ""





        

