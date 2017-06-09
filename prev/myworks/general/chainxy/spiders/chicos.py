
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

class Chicos(scrapy.Spider):
    name = "chicos"

    domain = "https://www.chicos.com"
    start_urls = ["https://stores.chicos.com/en/api/v2/stores.json"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.body)['stores']
        for store in store_list:
            item = ChainItem()
            if store['country_code'].find('US') != -1:
                item['country'] = "United States"
            elif store['country_code'].find('PR') != -1:
                item['country'] = "Puerto Rico"
            else:
                continue
                
            item['store_number'] =  store['id']
            item['country'] = store['country_code']
            item['latitude'] = store['latitude']
            item['longitude'] = store['longitude']
            item['store_name'] = store['name']
            item['other_fields'] = ""
            item['address'] = store['address_1']
            item['address2'] = self.validate(store['address_2'])
            item['city'] = store['city']
            item['state'] = store['state']
            item['zip_code'] = store['postal_code']
            item['phone_number'] =  store['phone_number']
            item['coming_soon'] = "0"
            item['store_hours'] = self.validate(store['business_hour_ranges'][0]['days']) + ':' + self.validate(store['business_hour_ranges'][0]['hours']) + "; " 
            try:
                item['store_hours'] = self.validate(store['business_hour_ranges'][1]['days']) + ':' + self.validate(store['business_hour_ranges'][2]['hours']) + "; " 
            except:
                pass

            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-').replace('&#8211;', '-').replace(u'\u2013', '-')
        else:
            return ""






        

