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

class Bubbas33(scrapy.Spider):
    name = "bubbas33"

    domain = "https://bubbas33.com/"
    start_urls = ["https://bubbas33.com/locations"]
    store_id = []

    def parse(self, response):
        store_ids = response.xpath("//script[contains(., 'window.locations = [{')]/text()").extract_first().split('window.locations = [{')[1].strip().split('"StoreId":')
        for store_id in store_ids[1:]:
            _id = store_id.split(',"Name"')[0].strip()
            yield scrapy.Request(url= "https://bubbas33.com/location-details/Index?storeId=%s" % _id, callback=self.parse_store)
    
    def parse_store(self, response):
        store = json.loads(response.body)
        item = ChainItem()
        item['store_number'] = store['StoreId']
        item['country'] = 'United States'
        item['latitude'] = store['Latitude']
        item['longitude'] = store['Longitude']
        item['other_fields'] = ""
        item['coming_soon'] = "0"
        item['store_hours'] = ""
        if store['Hours']['MonHours'].strip() != "-":
            item['store_hours'] += "Mon: " + store['Hours']['MonHours'] + ";"
        if store['Hours']['MonHours'].strip() != "-":
            item['store_hours'] += "Tue: " + store['Hours']['TueHours'] + ";"
        if store['Hours']['MonHours'].strip() != "-":
            item['store_hours'] += "Wed: " + store['Hours']['WedHours'] + ";"
        if store['Hours']['MonHours'].strip() != "-":
            item['store_hours'] += "Thu: " + store['Hours']['ThuHours'] + ";"
        if store['Hours']['MonHours'].strip() != "-":
            item['store_hours'] += "Fri: " + store['Hours']['FriHours'] + ";"
        if store['Hours']['MonHours'].strip() != "-":
            item['store_hours'] += "Sat: " + store['Hours']['SatHours'] + ";"
        if store['Hours']['MonHours'].strip() != "-":
            item['store_hours'] += "Sun: " + store['Hours']['SunHours'] + ";"

        item['store_name'] = store['Name']
        if item['store_name'].find('Opening') != -1:
            item['store_name'] = item['store_name'].split('(')[0]
            item['coming_soon'] = "1"
        item['address'] = store['Address1']
        item['address2'] = store['Address2']
        item['city'] = store['City']
        item['state'] = store['State']
        item['zip_code'] = store['Zip']
        item['phone_number'] =  store['Phone']
        yield item
    
    def validate(self, value):
        if value != None and value.strip() == '':
            return value
        else:
            return ""





        

