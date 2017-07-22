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
import usaddress

class Agjeans(scrapy.Spider):
    name = "agjeans"

    domain = "http://www.agjeans.com/"
    phone_number = []

    def __init__(self):
        cities_us = open('cities_us.json', 'rb')
        self.cities_list = json.load(cities_us)

    def start_requests(self):
        # for city in self.cities_list:
            # request_url = "http://www.agjeans.com/on/demandware.store/Sites-AGJeans-Site/default/Stores-GetNearestStores?latitude="+str(city['latitude'])+"&longitude="+str(city['longitude'])+"&countryCode=US&distanceUnit=mi&maxdistance=15000"
        request_url = "http://www.agjeans.com/on/demandware.store/Sites-AGJeans-Site/default/Stores-GetNearestStores?latitude=37.09024&longitude=-95.71289100000001&countryCode=US&distanceUnit=mi&maxdistance=15000"
        yield scrapy.Request(url=request_url, callback=self.parse_store)

    def parse_store(self, response):
        try:
            store_list = json.loads(response.body)['stores']
            for store in store_list:
                store = store_list[store]
                item = ChainItem()
                if store['phone'] in self.phone_number:
                    continue
                self.phone_number.append(store['phone'])
                item['phone_number'] =  store['phone']
                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = store['latitude']
                item['longitude'] = store['longitude']
                item['store_name'] = store['name']
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['address'] = store['address1']
                item['address2'] = self.validate(store['address2'])
                item['city'] = store['city']
                item['state'] = store['stateCode']
                item['zip_code'] = store['postalCode']

                item['store_hours'] = store['storeHours'].replace('<br>', ';')
                yield item
        except:
            return
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-').replace('&#8217;', "'")
        else:
            return ""

    def parse_citystatezip(self, value):
        city = self.validate(value.split(',')[0])
        state = self.validate(value.split(',')[1].strip().split(' ')[0])
        zip_code = self.validate(value.split(',')[1].strip().split(' ')[-1])
        return (city, state, zip_code)





        

