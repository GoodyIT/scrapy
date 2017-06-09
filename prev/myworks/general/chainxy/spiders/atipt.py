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

class Atipt(scrapy.Spider):
    name = "atipt"

    domain = "https://www.atipt.com/"
    start_urls = ["https://locator-api.localsearchprofiles.com/api/LocationSearchResults/?configuration=906b6529-84b4-4bae-ace2-ea68cb06201b&&searchby=address&address=36.704555%2C-76.595566"]
    store_id = []

    def start_requests(self):
        for x in xrange(0,700, 10):
            yield scrapy.Request(url="https://locator-api.localsearchprofiles.com/api/LocationSearchResults/?configuration=906b6529-84b4-4bae-ace2-ea68cb06201b&&searchby=address&address=36.704555%2C-76.595566&start=" + str(x), callback=self.parse_store)

    def parse_store(self, response):
        store_list = json.loads(response.body)['Hit']
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store['Fields']['LocationId']
            item['country'] = 'United States'
            item['latitude'] = self.validate(store['Fields']['Latlng']).split(',')[0]
            item['longitude'] = self.validate(store['Fields']['Latlng']).split(',')[1]
            item['store_name'] = ''
            item['other_fields'] = ""
            item['coming_soon'] = self.validate(store['Fields']['ComingSoon'])
            item['address'] = self.validate(store['Fields']['Address1'])
            try:
                item['address2'] = self.validate(store['Fields']['Address2'])
            except:
                item['address2'] = ''
            item['city'] = self.validate(store['Fields']['City'])
            item['state'] = self.validate(store['Fields']['State'])
            item['zip_code'] = self.validate(store['Fields']['Zip'])
            item['phone_number'] =  self.validate(store['Fields']['PhoneDisplay'])

            try:
                item['store_hours'] = self.hour_validate("Mon", store['HoursOfOperation']['Mon']) + self.hour_validate("Tue", store['HoursOfOperation']['Tue']) + self.hour_validate("Wed", store['HoursOfOperation']['Wed']) + self.hour_validate("Thu", store['HoursOfOperation']['Thu']) + self.hour_validate("Fri", store['HoursOfOperation']['Fri']) + self.hour_validate("Sat", store['HoursOfOperation']['Sat']) + self.hour_validate("Sun", store['HoursOfOperation']['Sun'])
            except:
                item['store_hours'] = ''
      
            yield item
    
    def validate(self, value):
        try:
            return value[0];
        except:
            return ""

    def hour_validate(self, day, hour):
        try:
            return day + ':' + hour['Hours'][0]['OpenTime'] + '-' + hour['Hours'][0]['CloseTime'] + ';'
        except Exception as e:
            raise e





        

