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

class Foodmaxx(scrapy.Spider):
    name = "foodmaxx"

    domain = "http://www.foodmaxx.com/"
    start_urls = ["https://momentfeed-prod.apigee.net/api/llp.json?auth_token=XPJMIEHNDDMYXTMA&coordinates=-9.96885060854611,-16.34765625,70.4367988185464,-175.78125&pageSize=500"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.body)
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store['store_info']['corporate_id']
            item['country'] = 'United States'
            item['latitude'] = store['store_info']['latitude']
            item['longitude'] = store['store_info']['longitude']
            item['store_name'] = store['store_info']['name']
            item['other_fields'] = ""
            item['address'] = store['store_info']['address']
            item['address2'] = ''
            item['city'] = store['store_info']['locality']
            item['state'] = store['store_info']['region']
            item['zip_code'] = store['store_info']['postcode']
            item['phone_number'] =  store['store_info']['phone']

            item['store_hours'] = "Monday " + "12:00 am - 12:00 am" + "; Tuesdays " + "12:00 am - 12:00 am" + "; Wednesday " + "12:00 am - 12:00 am" + "; Thursday " + "12:00 am - 12:00 am" + "; Friday " + "12:00 am - 12:00 am" + "; Saturday " + "12:00 am - 12:00 am" + "; Sunday " + "12:00 am - 12:00 am"
      
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

