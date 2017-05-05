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
            item['store_name'] = store_info.xpath('.//a/text()').extract_first()
            address = store_info.extract()
            request_url = "http://www.beddingexperts.com" + store_info.xpath('.//@href').extract()
            request = scrapy.Request(url=request_url, callback=self.parse_hours)
            request.meta['address'] = address
            request.meta['store_name'] = item['store_name']
            yield request

    def parse_hours(self, response):
        item = ChainItem()
        item['store_number'] = ""
        item['store_name'] = response.meta['store_name']
        address = response.meta['address']
        item['city'] = address[1].split(',')[0]
        item['state'] = store_info['state']
        item['zip_code'] = store_info['zip']
        item['address'] = address[0].strip()
        item['address2'] = ''
        item['country'] = 'United States'
        item['phone_number'] = address[2].strip()
        item['latitude'] = ''
        item['longitude'] = ''
        item['store_hours'] = ""
        item['other_fields'] = ""
        item['coming_soon'] = "0"

        yield item

    def validate(self, value):
        if type(value) == "str":
            return value
        else:
            return ""





        

