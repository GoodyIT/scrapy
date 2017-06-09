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

class Volvocars(scrapy.Spider):
    name = "volvocars"

    domain = "http://www.volvocars.com/"
    start_urls = ["http://www.volvocars.com/data/dealers?marketSegment=%2Fus&expand=Services%2CUrls&format=json&northToSouthSearch=False&filter=MarketId+eq+%27us%27+and+LanguageId+eq+%27en%27"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.body)
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store['DealerId']
            item['country'] = 'United States'
            item['latitude'] = store['GeoCode']['Latitude']
            item['longitude'] = store['GeoCode']['Longitude']
            item['store_name'] = store['Name']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store['AddressLine1']
            item['address2'] = store['AddressLine2']
            item['city'] = store['City']
            item['state'] = store['District']
            item['zip_code'] = store['ZipCode']
            item['phone_number'] =  store['Phone']

            item['store_hours'] = ''
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

