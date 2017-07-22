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
from datetime import datetime, timedelta

class Bridgestonetire(scrapy.Spider):
    name = "bridgestonetire"

    domain = "http://www.bridgestonetire.com/"
    store_number = []

    def __init__(self):
        ca_json = open('citiesusca.json', 'rb')
        self.ca_long_lat_fp = json.load(ca_json)
        

    def start_requests(self):
        for city in self.ca_long_lat_fp:
            if self.ca_long_lat_fp[city]["country"] == "United States":
                request_url = "http://www.bridgestonetire.com/bin/bridgestone/consumer/bst/api/v1/stores/nearbystores.json?callback=jQuery22409025644305165341_1498052563451&country=US&lat="+str(self.ca_long_lat_fp[city]['latitude'])+"&lon="+str(self.ca_long_lat_fp[city]['longitude'])+"&_=1498052563458"
                yield scrapy.Request(url=request_url, callback=self.parse_store)

    def parse_store(self, response):
        try:
            json_body = response.body.replace('jQuery22409025644305165341_1498052563451(', '')[:-2].decode('raw-unicode-escape')
            # if (len(json_body) == 2):
            #     return;
            store_list = json.loads(json_body)
            for store in store_list:
                item = ChainItem()
                if store['country'] != 'us':
                    return
                if store['storeNumber'] in self.store_number:
                    continue
                self.store_number.append(store['storeNumber'])
                item['phone_number'] =  store['phoneNumber']
                item['store_number'] = store['storeNumber']
                item['country'] = 'United States'
                item['latitude'] = store['latitude']
                item['longitude'] = store['longitude']
                item['store_name'] = store['name']
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['address'] = store['streetAddress']
                item['address2'] = ''
                item['city'] = store['city']
                item['state'] = self.validate(store['province'])
                item['zip_code'] = self.validate(store['postalCode'])

                item['store_hours'] = "Mon:" + self.parse_time(store['mondayHours']['openTime'])  + " - " +  self.parse_time(store['mondayHours']['closeTime']) + '; '+"Tue:" + self.parse_time(store['tuesdayHours']['openTime'])  + " - " +  self.parse_time(store['tuesdayHours']['closeTime']) + '; '+"Wed:" + self.parse_time(store['wednesdayHours']['openTime'])  + " - " +  self.parse_time(store['wednesdayHours']['closeTime']) + '; '+"Thu:" + self.parse_time(store['thursdayHours']['openTime'])  + " - " +  self.parse_time(store['thursdayHours']['closeTime']) + '; '+"Fri:" + self.parse_time(store['fridayHours']['openTime'])  + " - " +  self.parse_time(store['fridayHours']['closeTime']) + '; '+"Sat:" + self.parse_time(store['saturdayHours']['openTime'])  + " - " +  self.parse_time(store['saturdayHours']['closeTime']) + '; '+"Sun:" + self.parse_time(store['sundayHours']['openTime'])  + " - " +  self.parse_time(store['sundayHours']['closeTime']) + '; '

                yield item
        except:
            pdb.set_trace()
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-').replace('&#8217;', "'")
        else:
            return ""

    def parse_time(self, value):
        try:
            return (datetime.fromtimestamp(int(value)/1000)+timedelta(hours=3)).strftime('%I:%M %p')
        except:
            return ""

