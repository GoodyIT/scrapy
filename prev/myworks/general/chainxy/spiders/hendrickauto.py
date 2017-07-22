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

class Hendrickauto(scrapy.Spider):
    name = "hendrickauto"

    domain = "http://http://www.hendrickauto.com/"
    start_urls = ["http://www.hendrickauto.com/locations/index.htm"]
    store_id = []
    store_name = []

    def parse(self, response):
        store_list = response.xpath('.//li[contains(@class, "vcard")]')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_name'] = store.xpath('.//a/span/text()').extract_first()
            if item['store_name'] in self.store_name:
                pass;
            self.store_name.append(item['store_name'])

            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store.xpath('.//span[@class="street-address"]/text()').extract_first()
            item['address2'] =  ''
            item['city'] = store.xpath('.//span[@class="locality"]/text()').extract_first()
            item['state'] = store.xpath('.//span[@class="region"]/text()').extract_first()
            item['zip_code'] = store.xpath('.//span[@class="postal-code"]/text()').extract_first()
            item['phone_number'] = ''

            item['store_hours'] = ''
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

