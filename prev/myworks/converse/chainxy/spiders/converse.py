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

class Converse(scrapy.Spider):
    name = "converse"

    domain = "www.nike.com/us/en_us/c/converse"
    start_urls = ["http://www.nike.com/us/en_us/retail/en/api/v2/stores.json"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_list = json.loads(response.body)['stores']
        for store_info in store_list:
            if store_info['country_code'] != "US":
                continue

            item = ChainItem()

            if store_info['id'] in self.store_id:
                continue
            self.store_id.append(store_info['id'])
            item['store_number'] =  store_info['id']
            item['store_name'] = store_info['type']['name']
            item['city'] = store_info['city']
            item['state'] = store_info['state']
            item['zip_code'] = store_info['postal_code']
            item['address'] = store_info['address_1']
            item['address2'] = store_info['address_2']
            item['country'] = "United States"
            item['phone_number'] = store_info['phone_number']
            item['latitude'] = store_info['latitude']
            item['longitude'] = store_info['longitude']

            item['store_hours'] = ""
            try:
                sun = store_info['regular_hour_ranges'][0]
                mon_sat = store_info['regular_hour_ranges'][1]
                item['store_hours'] += sun['days'] + self.validate(sun['hours']) + "; " + mon_sat['days'].replace(u'\u2013', '~') + self.validate(mon_sat['hours'])
            except:
                item['store_hours'] = ""
               
            item['other_fields'] = ""
            item['coming_soon'] = "0"    
            yield item


    def validate(self, value):
        return value.replace('&#8211;', '-')







        

