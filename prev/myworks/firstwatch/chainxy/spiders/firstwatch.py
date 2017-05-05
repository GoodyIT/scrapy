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

class Firstwatch(scrapy.Spider):
    name = "firstwatch"

    domain = "http://www.firstwatch.com/"
    start_urls = ["https://www.firstwatch.com/zsapi/locations/"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        pdb.set_trace()
        store_list = json.loads(response.body)
        for store_info in store_list:
            item = ChainItem()

            item['store_number'] = store_info['brandChaindId']
            item['store_name'] = store_info['name']
            item['city'] = store_info['address']['city']
            item['state'] = store_info['address']['region']
            item['zip_code'] = store_info['address']['zip']
            item['address'] = store_info[address]['address1']
            item['address2'] = store_info[address]['address2']
            item['country'] = 'United States'
            item['phone_number'] = store_info['phone1']
            item['latitude'] = store_info['address']['loc'][0]
            item['longitude'] = store_info['address']['loc'][1]

            try:
                hours = store_info['hours']['sets'][0]['days']
                mon = "Monday: " + self.validate(hours['mon'][0]['start']) + '-' + self.validate(hours['mon'][0]['end'])
                tue = "Tuesday " + self.validate(hours['tue'][0]['start']) + '-' + self.validate(hours['tue'][0]['end'])
                wed = "Wednsday " + self.validate(hours['wed'][0]['start']) + '-' + self.validate(hours['wed'][0]['end'])
                thus = "Thursday " + self.validate(hours['thu'][0]['start']) + '-' + self.validate(hours['thu'][0]['end'])
                fri = "Friday " + self.validate(hours['fri'][0]['start']) + '-' + self.validate(hours['fri'][0]['end'])
                sat = "Saturday" + self.validate(hours['sat'][0]['start']) + '-' + self.validate(hours['sat'][0]['end'])
                sun = "Sunday" +  self.validate(hours['sun'][0]['start']) + '-' + self.validate(hours['sun'][0]['end'])
                
                item['store_hours'] = ""
                if store_info['status'] == "Open":
                    item['store_hours'] += mon + ";"
                else:
                    item['store_hours'] += "Moday: close;"
                if store_info['status'] == "Open":
                    item['store_hours'] += tue + ";"
                else:
                    item['store_hours'] += "Tuesday: close;"
                if store_info['status'] == "Open":
                    item['store_hours'] += wed + ";"
                else:
                    item['store_hours'] += "Wedsday: close;"
                if store_info['status'] == "Open":
                    item['store_hours'] += thus + ";"
                else:
                    item['store_hours'] += "Thursday: close;"
                if store_info['status'] == "Open":
                    item['store_hours'] += fri + ";"
                else:
                    item['store_hours'] += "Friday: close;"
                if store_info['status'] == "Open":
                    item['store_hours'] += sat + ";"
                else:
                    item['store_hours'] += "Saturday: close;"
                if store_info['status'] == "Open":
                    item['store_hours'] += sun + ";"
                else:
                    item['store_hours'] += "Sunday: close;"
            except:
                item['store_hours'] = ""
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                
            yield item


    def validate(self, value):
        if int(value) / 60 < 12:
            return int(value) / 60 + ":00am"
        else:
            int(value) / 60 + ":00pm"







        

