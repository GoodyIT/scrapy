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
from lxml import html

class Atlanticsuperstore(scrapy.Spider):
    name = "atlanticsuperstore"

    domain = "https://www.atlanticsuperstore.ca/"
    start_urls = ["https://www.atlanticsuperstore.ca/store-locator/locations/all?showNonShoppable=true"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.body)['searchResult']
        for store in store_list:
            request = scrapy.Request(url="https://www.atlanticsuperstore.ca" + store['details']['url'], callback=self.parse_store)
            request.meta['store'] = store
            yield request

    def parse_store(self, respone):
        store = respone.meta['store']
        item = ChainItem()
        item['store_number'] = store['details']['storeID']
        item['country'] = 'Canada'
        item['latitude'] = store['lat']
        item['longitude'] = store['lng']
        item['store_name'] = store['details']['storeName']
        item['other_fields'] = ""
        item['coming_soon'] = "0"
        item['address'] = store['details']['streetAddress']
        item['address2'] = ''
        item['city'] = store['details']['city']
        item['state'] = store['details']['province']
        item['zip_code'] = store['details']['postalCode']
        item['phone_number'] = respone.xpath('.//div[@class="contact"]/p[1]/text()').extract_first().strip()
        hours = respone.xpath('.//div[@class="hours"]/p')
        item['store_hours'] = ''
        for hour in hours[:6]:
            temp = hour.xpath('.//text()').extract()
            temp = [tp.strip().replace('\n', '').replace('\r', '') for tp in temp if tp.strip() != ""]
            item['store_hours'] += ''.join(temp) + '; '
        
        yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

