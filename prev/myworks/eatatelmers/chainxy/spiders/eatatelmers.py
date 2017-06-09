# -*- coding: utf-8 -*-
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

import os, sys

import pdb

class Eatatelmers(scrapy.Spider):
    name = "eatatelmers"

    domain = "https://eatatelmers.com/"
    start_urls = ["https://eatatelmers.com/wp-admin/admin-ajax.php"]
    store_id = []

    def start_requests(self):
        yield FormRequest(url=self.start_urls[0], formdata={ "address":'', "formdata":'nameSearch=&addressInput=&addressInputCity=&addressInputState=&addressInputCountry=&ignore_radius=0', 'lat':'45.5113506', "lng":'-122.64567390000002',"name":'', 'radius':'10000', 'tags':'', 'action':'csl_ajax_onload'}, headers={'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'*/*', 'Accept-Language':'en-US,en;q=0.8', 'X-Requested-With':'XMLHttpRequest'}, callback=self.parse_store)
    
    def parse_store(self, response):
        store_list = json.loads(response.body)['response']
        for store in store_list:
            item = ChainItem()

            item['store_number'] = store['id']
            item['store_name'] = self.validate(store['name'])
            item['address2'] = self.validate(store['address2'])
            item['address'] = self.validate(item['store_name'])
            item['country'] = 'United States'
            item['city'] = self.validate(store['city'])
            item['state'] = self.validate(store['state'])
            item['zip_code'] = self.validate(store['zip'])
            item['phone_number'] = self.validate(store['phone'])
            item['store_hours'] = self.validate(store['hours'])
            item['coming_soon'] = "0"
            item['store_hours'] = ''
            item['latitude'] = self.validate(store['lat'])
            item['longitude'] = self.validate(store['lng'])

            item['other_fields'] = ''

            if item['phone_number'].find('Coming') != -1:
                item['phone_number'] = ''
                item['coming_soon'] = "1"
            
            yield item
   

    def validate(self, value):
        if value == None:
            return ""
        else:
            return value.replace('&#039;', "'").strip()




        

