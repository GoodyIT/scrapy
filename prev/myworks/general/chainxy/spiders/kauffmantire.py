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

class Kauffmantire(scrapy.Spider):
    name = "kauffmantire"

    domain = "https://www.kauffmantire.com/"
    start_urls = ["https://kcomapi.kauffmantire.com/api/v1.0/stores?ship-zip-code=33629&mile-range=750000&trackid=1234"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.body)['response']['storeData']
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store['storeOrder']
            item['country'] = 'United States'
            item['latitude'] = store['latitude']
            item['longitude'] = store['longitude']
            item['store_name'] = store['name']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store['address']
            item['address2'] = store['address2']
            item['city'] = store['city']
            item['state'] = store['state']
            item['zip_code'] = store['zipcode']
            item['phone_number'] =  store['phone']

            item['store_hours'] = store['hours'].replace(',', ';')
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

