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

class Christiedental(scrapy.Spider):
    name = "christiedental"

    domain = "https://www.christiedental.com/"
    start_urls = ["https://www.christiedental.com/wp-admin/admin-ajax.php"]
    store_id = []

    def start_requests(self):
        yield FormRequest(url="https://www.christiedental.com/wp-admin/admin-ajax.php", formdata={"action":"prov_search","data[search_type]":"all", "data[lat]":"28.5383", "data[lng]":"-81.3792"}, callback=self.parse_store)

    def parse_store(self, response):
        store_list = json.loads(response.body)['results']
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store['id']
            item['country'] = 'United States'
            item['latitude'] = store['lat']
            item['longitude'] = store['lng']
            item['store_name'] = store['name']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store['address1']
            item['address2'] = store['address2']
            item['city'] = store['city']
            item['state'] = store['state']
            item['zip_code'] = store['postal_code']
            item['phone_number'] =  store['phone_primary']

            mon = ''
            if store['hours']['Monday'][0].strip() != '':
                mon = "Monday: " + store['hours']['Monday'][0] + '-' + store['hours']['Monday'][1] + "; "
            tue = ''
            if store['hours']['Tuesday'][0].strip() != '':
                tue = "Tuesday: " + store['hours']['Tuesday'][0] + '-' + store['hours']['Tuesday'][1] + "; "
            wed = ''
            if store['hours']['Wednesday'][0].strip() != '':
                mon = "Wednesday: " + store['hours']['Wednesday'][0] + '-' + store['hours']['Wednesday'][1] + "; "
            thu = ''
            if store['hours']['Thursday'][0].strip() != '':
                thu = "Thursday: " + store['hours']['Thursday'][0] + '-' + store['hours']['Thursday'][1] + "; "
            fri = ''
            if store['hours']['Friday'][0].strip() != '':
                fri = "Friday: " + store['hours']['Friday'][0] + '-' + store['hours']['Friday'][1] + "; "
            sat = ''
            if store['hours']['Saturday'][0].strip() != '':
                sat = "Saturday: " + store['hours']['Saturday'][0] + '-' + store['hours']['Saturday'][1] + "; "
            sun = ''
            if store['hours']['Sunday'][0].strip() != '':
                sun = "Sunday: " + store['hours']['Sunday'][0] + '-' + store['hours']['Sunday'][1] + "; "
            item['store_hours'] = mon + tue + wed + thu + fri + sat + sun + store['custom_hours']
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

