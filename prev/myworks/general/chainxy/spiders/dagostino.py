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

class Dagostino(scrapy.Spider):
    name = "dagostino"

    domain = "https://www.dagnyc.com/"
    start_urls = ["https://api.freshop.com/1/stores?limit=-1&has_address=true&token=63de2ba0e689c8b102d9954344ac7145&app_key=dagostino"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.body)['items']
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store['id']
            item['country'] = 'United States'
            item['latitude'] = store['latitude']
            item['longitude'] = store['longitude']
            item['store_name'] = store['name']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            try:
                item['address'] = store['address_0']
            except:
                item['address'] = store['address_1']
            item['address2'] = ''
            item['city'] = store['city']
            item['state'] = store['state']
            item['zip_code'] = store['postal_code']
            item['phone_number'] =  store['phone'].split('\n')[0]

            try:
                item['store_hours'] = store['hours']
            except:
                item['store_hours'] = store['hours_md']
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

