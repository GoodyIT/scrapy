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

class Toyota(scrapy.Spider):
    name = "toyota"

    domain = "https://www.toyota.com"
    start_urls = ["https://www.toyota.ca/toyota/data/dealer/.json"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.body)['dealers']
        for store in store_list:
            item = ChainItem()
            store = store_list[store]
            item['store_number'] = store['code']
            item['country'] = 'Canada'
            item['latitude'] = store['location']['lat']
            item['longitude'] = store['location']['lng']
            item['store_name'] = store['name']['en']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store['address']['streetAddress']
            item['address2'] = ''
            item['city'] = store['address']['city']
            item['state'] = store['address']['province']
            item['zip_code'] = store['address']['postalCode']
            item['phone_number'] =  store['phoneNumbers'][0]['CompleteNumber']

            try:
                item['store_hours']  = self.parse_time(store['departments'][2]['hours'])
            except:
                item['store_hours']  = self.parse_time(store['departments'][1]['hours'])

            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""

    def parse_time(self, value_list):
        hours = ''
        for value in value_list:
            hours += value['fromDay']['en'] +" "+ value['startTime']['en'] + " - " + value['endTime']['en'] + "; "    

        return hours





        

