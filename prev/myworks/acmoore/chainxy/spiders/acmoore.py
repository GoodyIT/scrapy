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

class acmoore(scrapy.Spider):
    name = "acmoore"

    domain = "http://www.acmoore.com/"
    start_urls = ["https://www.acmoore.com/lightspeed.php/dealerlocator/index/searchdealer"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_list = json.loads(response.body)
        for store_info in store_list:
            item = ChainItem()

            item['store_number'] = store_info['dealerlocator_id']
            item['store_name'] = store_info['dealer_name']
            item['city'] = store_info['city']
            item['state'] = store_info['state']
            item['zip_code'] = store_info['zip']
            item['address'] = store_info['address1']
            item['address2'] = store_info['address2']
            item['country'] = 'United States'
            item['phone_number'] = store_info['phone']
            item['latitude'] = store_info['latitude']
            item['longitude'] = store_info['longitude']

            try:
                hours = store_info['store_hours'][0]
                mon = "Monday: " + self.validate(hours['mon_start']) + '-' + self.validate(hours['mon_end'])
                tue = "Tuesday " + self.validate(hours['tue_start']) + '-' + self.validate(hours['tue_end'])
                wed = "Wednsday " + self.validate(hours['wed_start']) + '-' + self.validate(hours['wed_end'])
                thus = "Thursday " + self.validate(hours['thus_start']) + '-' + self.validate(hours['thus_end'])
                fri = "Friday " + self.validate(hours['fri_start']) + '-' + self.validate(hours['fri_end'])
                sat = "Saturday" + self.validate(hours['sat_start']) + '-' + self.validate(hours['sat_end'])
                sun = "Sunday" +  self.validate(hours['sun_start']) + '-' + self.validate(hours['sun_end'])
                
                item['store_hours'] = ""
                if hours['mon_start_openclose'] == "Open":
                    item['store_hours'] += mon + ";"
                else:
                    item['store_hours'] += "Moday: close;"
                if hours['tue_start_openclose'] == "Open":
                    item['store_hours'] += tue + ";"
                else:
                    item['store_hours'] += "Tuesday: close;"
                if hours['wed_start_openclose'] == "Open":
                    item['store_hours'] += wed + ";"
                else:
                    item['store_hours'] += "Wedsday: close;"
                if hours['thu_start_openclose'] == "Open":
                    item['store_hours'] += thus + ";"
                else:
                    item['store_hours'] += "Thursday: close;"
                if hours['fri_start_openclose'] == "Open":
                    item['store_hours'] += fri + ";"
                else:
                    item['store_hours'] += "Friday: close;"
                if hours['sat_start_openclose'] == "Open":
                    item['store_hours'] += sat + ";"
                else:
                    item['store_hours'] += "Saturday: close;"
                if hours['sun_start_openclose'] == "Open":
                    item['store_hours'] += sun + ";"
                else:
                    item['store_hours'] += "Sunday: close;"
            except:
                item['store_hours'] = ""
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                
            yield item


    def validate(self, value):
        if type(value) == "str":
            return value
        else:
            return ""





        

