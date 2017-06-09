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

class Visionworks(scrapy.Spider):
    name = "visionworks"

    domain = "https://www.visionworks.com"
    start_urls = ["http://www.85cbakerycafe.com/wp-admin/admin-ajax.php?action=store_search&lat=33.6881056&lng=-117.8339795&max_results=25&radius=50&autoload=1"]
    phone_number = []

    def __init__(self):
        ca_json = open('citiesusca.json', 'rb')
        self.ca_long_lat_fp = json.load(ca_json)

    def parse(self, response):
        for city in self.ca_long_lat_fp:
            if self.ca_long_lat_fp[city]["country"] == "United States":
                yield scrapy.Request(url="https://www.visionworks.com/misc/ajax/locators/locators.jsp?latitude=%s&longitude=%s" % (self.ca_long_lat_fp[city]["latitude"], self.ca_long_lat_fp[city]["longitude"]), callback=self.parse_store)
    
    def parse_store(self, response):
        store_list = json.loads(response.body)['markers']
        for store in store_list:
            item = ChainItem()
            item['phone_number'] =  store['tel']
            if store['tel'] in self.phone_number:
                continue
            self.phone_number.append(store['tel'])

            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = store['lat']
            item['longitude'] = store['lng']
            if len(store['name'].split('</b>')) == 2:
                item['store_name'] = store['name'].split('</b>')[1].strip()
            else:
                item['store_name'] = store['name']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store['address2']
            item['address2'] = store['address1']
            item['city'] = store['city']
            item['state'] = store['state']
            item['zip_code'] = store['zipCode']

            item['store_hours'] = ''
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

