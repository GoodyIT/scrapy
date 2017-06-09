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

class Cityfurniture(scrapy.Spider):
    name = "cityfurniture"

    domain = "http://www.cityfurniture.com/"
    start_urls = ["http://www.cityfurniture.com/find/ajax/stores"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.body)
        for store in store_list:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = store['Latitude']
            item['longitude'] = store['Longitude']
            item['store_name'] = store['Name']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store['Address']
            item['address2'] = ''
            item['city'] = store['City']
            item['state'] = store['State']
            item['zip_code'] = store['Zip']
            item['phone_number'] =  store['PhoneMain']
            hours = store['StoreHours'].split('<br>')
            hours = [tp.strip().replace('\n', '') for tp in hours if tp.strip() != ""]
            item['store_hours'] = ''
            for hour in hours:
                item['store_hours'] += html.fromstring(hour).xpath('.//span[1]/text()')[0] + html.fromstring(hour).xpath('.//span[2]/text()')[0] + "; "

            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

