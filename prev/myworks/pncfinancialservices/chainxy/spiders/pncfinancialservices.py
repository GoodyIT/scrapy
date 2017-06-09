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

class Pncfinancialservices(scrapy.Spider):
    name = "pncfinancialservices"

    domain = "https://apps.pnc.com/"
    start_urls = ["https://apps.pnc.com/locator-api/locator/api/v2/location/?t=1494571253713&latitude=%s&longitude=%s&radius=100&radiusUnits=mi&branchesOpenNow=false"]
    store_id = []

    def __init__(self):
        us_json = open('states.json', 'rb')

        self.us_long_lat_fp = json.load(us_json)

    def start_requests(self):
        for row in self.us_long_lat_fp:
            yield scrapy.Request(url= self.start_urls[0] % (row['latitude'], row['longitude']), callback=self.parse_store)
        
    def parse_store(self, response):
        store_list = json.loads(response.body)['locations']
        for store_info in store_list:
            item = ChainItem()

            if store_info["locationId"] in self.store_id:
                continue
            self.store_id.append(store_info["locationId"])

            try:
                item['store_number'] = store_info['locationId']
                item['store_name'] = store_info['locationName']
                item['address'] = self.validate(store_info['address']['address1'])
                item['address2'] = self.validate(store_info['address']['address2'])
                item['city'] = self.validate(store_info['address']['city'])
                item['state'] = self.validate(store_info['address']['state'])
                item['zip_code'] = self.validate(store_info['address']['zip'])
                item['country'] = 'United States'
                try:
                    item['phone_number'] = store_info['contactInfo'][0]['contactInfo']
                except:
                    item['phone_number'] = ''
                item['latitude'] = store_info['address']['latitude']
                item['longitude'] = store_info['address']['longitude']
                item['store_hours'] = ''
                item['other_fields'] = ""
                item['coming_soon'] = "0"
            except:
                pdb.set_trace()
                    
                yield item

    def validate(self, value):
        if value != None:
            return value
        else:
            return ""





        

