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

class Valumart(scrapy.Spider):
    name = "valumart"

    domain = "http://www.valumart.ca/"
    start_urls = ["https://www.valumart.ca/store-locator/locations/all?showNonShoppable=true"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_list = json.loads(response.body)['searchResult']
        for store_info in store_list:
            item = ChainItem()
            request_url = "https://www.valumart.ca" + store_info['details']['url']
            request = scrapy.Request(url=request_url, callback=self.parse_hours)
            request.meta['store_info'] = store_info
                
            yield request

    def parse_hours(self, response):
            item = ChainItem()
            store_info = response.meta['store_info']
            item['store_number'] = store_info['details']['storeID']
            item['store_name'] = store_info['details']['storeName']
            item['city'] = store_info['details']['city']
            item['state'] = store_info['details']['province']
            item['zip_code'] = store_info['details']['postalCode']
            item['address'] = store_info['details']['streetAddress']
            item['address2'] = ''
            item['country'] = 'Canada'
            item['phone_number'] = ''
            item['latitude'] = store_info['lat']
            item['longitude'] = store_info['lng']

            hours = response.xpath('//div[@class="hours"]/p')
            item['store_hours'] = ''
            for hour in hours:
                item['store_hours'] += hour.xpath('.//text()').extract()[1].strip() + hour.xpath('.//text()').extract()[2].strip()
            item['other_fields'] = ""
            item['coming_soon'] = "0"

            yield item

    def validate(self, value):
        if type(value) == "str":
            return value
        else:
            return ""





        

