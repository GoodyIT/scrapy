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

class Theproteinbar(scrapy.Spider):
    name = "theproteinbar"

    domain = "http://biscuitscafe.com/"
    start_urls = ["https://www.theproteinbar.com/data/datalayer.json"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.body)['Locations']
        for store in store_list:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = store['latitude']
            item['longitude'] = store['longitude']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['store_hours'] = store['hours summary'].replace('[b]', '').replace('[/b]', '').replace('&', ';').replace('|', ';')
            item['store_name'] = store['restaurant']
            item['address'] = store['street address']
            item['address2'] = ''
            item['city'] = store['city']
            item['state'] = store['state']
            item['zip_code'] = store['zip']
            item['phone_number'] =  store['phone']
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

