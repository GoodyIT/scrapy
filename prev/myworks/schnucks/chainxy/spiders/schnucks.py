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

class Schnucks(scrapy.Spider):
    name = "schnucks"

    domain = "http://www.schnucks.com/"
    start_urls = ["https://dataservices.schnucks.com/json/query_stores.json?callback=jQuery112405159340269675581_1494215594526&deptid=ALL&servid=ALL&_=1494215594527"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_list = json.loads(response.body.split('jQuery112405159340269675581_1494215594526(')[1].strip().split(');')[0].strip())['stores']
        for store_info in store_list:
            item = ChainItem()

            item['store_number'] = store_info['STORE']
            item['store_name'] = store_info['WEB_STORE_NAME']
            item['city'] = store_info['CITY']
            item['zip_code'] = store_info['ZIP']
            item['address'] = store_info['ADDRESS']
            item['address2'] = ''
            item['country'] = 'United States'
            item['phone_number'] = store_info['PHONE']
            item['latitude'] = store_info['LATITUDE']
            item['longitude'] = store_info['LONGITUDE']

            item['state'] = ''
            item['store_hours'] = store_info['HOURS']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
                
            yield item

    def validate(self, value):
        if type(value) == "str":
            return value
        else:
            return ""





        

