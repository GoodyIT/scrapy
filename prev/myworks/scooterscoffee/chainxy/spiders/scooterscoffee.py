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

class Scooterscoffee(scrapy.Spider):
    name = "scooterscoffee"

    domain = "http://www.scooterscoffee.com/"
    start_urls = ["https://www.scooterscoffee.com/data/locations.json?origLat=38.0608445&origLng=-97.92977429999996&origAddress=Hutchinson,+KS"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_list = json.loads(response.body)
        for store_info in store_list:
            item = ChainItem()

            item['store_number'] = ''
            item['store_name'] = store_info['name'].replace(u'\u200b','')
            item['city'] = store_info['city']
            item['state'] = store_info['state']
            item['zip_code'] = store_info['postal']
            item['address'] = store_info['address'].replace(u'\u200b', '')
            item['address2'] = ''
            item['country'] = 'United States'
            item['phone_number'] = store_info['phone']
            item['latitude'] = store_info['lat']
            item['longitude'] = store_info['lng']

            item['store_hours'] = ""
            if store_info['hours1'] != "":
                item['store_hours'] += store_info['hours1'] + "; "
            if store_info['hours2'] != "":
                item['store_hours'] += store_info['hours2'] + "; "
            if store_info['hours3'] != "":
                item['store_hours'] += store_info['hours3'] + "; "
            if store_info['hours4'] != "":
                item['store_hours'] += store_info['hours4'] + "; "
                
            item['other_fields'] = ""
            item['coming_soon'] = "0"
                
            yield item


    def validate(self, value):
        if type(value) == "str":
            return value
        else:
            return ""





        

