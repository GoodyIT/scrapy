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

class Beddingexperts(scrapy.Spider):
    name = "beddingexperts"

    domain = "http://www.beddingexperts.com/"
    start_urls = ["http://www.beddingexperts.com/mattress-stores-locator-retail-locations/default.aspx"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_list = response.xpath('//p[@class="padT5 padL10 padB5"]')
        for store_info in store_list:
            store_name = store_info.xpath('.//a/text()').extract_first()
            address = store_info.xpath('.//text()').extract()
            request_url = "http://www.beddingexperts.com" + store_info.xpath('.//@href').extract_first() + '/'
            request = scrapy.Request(url=request_url, callback=self.parse_hours)
            request.meta['address'] = address
            request.meta['store_name'] = store_name
            yield request

    def parse_hours(self, response):
        item = ChainItem()
        item['store_number'] = ""
        item['store_name'] = response.meta['store_name']

        address = response.meta['address']
        item['address'] = address[1]
        address1 = address[-2]
        item['city'] = address1.split(',')[0]
        item['state'] = address1.split(',')[1].strip().split(' ')[0]
        item['zip_code'] = address1.split(',')[1].strip().split(' ')[1]
       
        item['country'] = 'United States'
        item['phone_number'] = address[-1].replace('Phone:', '').strip()
        item['latitude'] = ''
        item['longitude'] = ''
        hours = response.xpath('//div[@id="dvStoreDescription"]/ul/li/text()').extract()
        item['store_hours'] = "; ".join(hours)
        item['other_fields'] = ""
        item['coming_soon'] = "0"

        yield item

    def validate(self, value):
        if type(value) == "str":
            return value
        else:
            return ""





        

