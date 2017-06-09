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

class Jazzercise(scrapy.Spider):
    name = "jazzercise"

    domain = "http://jcls.jazzercise.com"
    start_urls = ["http://jcls.jazzercise.com/search/getmarkers?search=%s,%s&lat=%s&lng=%s&distance=250&returnvalue=Miles"]
    store_id = []

    def __init__(self):
        us_json = open('states.json', 'rb')
        ca_json = open('citiesusca.json', 'rb')

        self.us_long_lat_fp = json.load(us_json)
        self.ca_long_lat_fp = json.load(ca_json)

    def start_requests(self):
        for row in self.us_long_lat_fp:
            yield scrapy.Request(url= self.start_urls[0] % (row['name'], "US", row['latitude'], row['longitude']), callback=self.parse_store)
        
        for city in self.ca_long_lat_fp:
            if self.ca_long_lat_fp[city]["country"] == "Canada":
                yield scrapy.Request(url= self.start_urls[0] % (self.us_long_lat_fp[city]["state"], "Canada", self.us_long_lat_fp[city]["latitude"], self.us_long_lat_fp[city]["longitude"]), callback=self.parse_store)

    def parse_store(self, response):
        store_list = json.loads(response.body)
        for store_info in store_list:
            item = ChainItem()

            if store_info["id"] in self.store_id:
                continue
            self.store_id.append(store_info["id"])

            try:
                item['store_number'] = store_info['id']
                item['store_name'] = store_info['name']
                item['address'] = store_info['address']
                item['address2'] = ''
                item['city'] = store_info['citystatezip'].split(',')[0].strip()
                item['state'] = store_info['citystatezip'].split(',')[1].strip().split(' ')[0]
                try:
                    item['zip_code'] = store_info['citystatezip'].split(',')[1].strip().split(' ')[1]
                except:
                    item['zip_code'] = ''
                item['country'] = 'United States'
                item['phone_number'] = store_info['phone']
                item['latitude'] = store_info['lat']
                item['longitude'] = store_info['lng']
                item['store_hours'] = ''
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                if store_info['comingdate'] == 'true':
                    item['coming_soon'] = "1"
            except:
                pdb.set_trace()
                    
                yield item

    def validate(self, value):
        if type(value) == "str":
            return value
        else:
            return ""





        

