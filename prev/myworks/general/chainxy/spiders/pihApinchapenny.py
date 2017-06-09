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

class PihApinchapenny(scrapy.Spider):
    name = "pihApinchapenny"

    domain = "https://pinchapenny.com/"
    start_urls = ["https://pinchapenny.com/stores"]
    store_id = []

    def __init__(self):
        ca_json = open('citiesusca.json', 'rb')
        self.ca_long_lat_fp = json.load(ca_json)

    def parse(self, response):
        token = response.xpath('.//input[@name="_token"]/@value').extract_first()
        for city in self.ca_long_lat_fp:
            if self.ca_long_lat_fp[city]["country"] == "United States":
                for x in xrange(1,3):
                    formdata = {
                        "_token":str(token),
                        "lat":str(self.ca_long_lat_fp[city]["latitude"]),
                        "lng":str(self.ca_long_lat_fp[city]["longitude"]),
                        "has_service":"0",
                        "has_bge":"0",
                        "has_repair":"0"
                    }
                    
                    yield FormRequest(url="https://pinchapenny.com/stores/search?page=" + str(x), headers={"Content-Type": "application/x-www-form-urlencoded"}, formdata=formdata, callback=self.parse_store)
        
    def parse_store(self, response):
        store_list = json.loads(response.body)['data']
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store['id']
            if store['id'] in self.store_id:
                continue
            self.store_id.append(store['id'])
            item['country'] = 'United States'
            item['latitude'] = store['latitude']
            item['longitude'] = store['longitude']
            item['store_name'] = store['name']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store['address']
            item['address2'] = store['address_extended']
            item['city'] = store['locality']
            item['state'] = store['region']
            item['zip_code'] = store['postcode']
            item['phone_number'] =  store['phone']

            try:
                item['store_hours'] = store['store_hours_microdata']['Monday'] + "; " +store['store_hours_microdata']['Tuesday'] + "; " + store['store_hours_microdata']['Wednesday'] + "; " + store['store_hours_microdata']['Thursday'] + "; " + store['store_hours_microdata']['Friday'] + "; " + store['store_hours_microdata']['Saturday'] + "; " + store['store_hours_microdata']['Sunday']
            except:
                item['store_hours'] = ''

            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

