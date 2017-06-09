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
import geocoder
import time

class Shoppersworldusa(scrapy.Spider):
    name = "shoppersworldusa"

    domain = "http://www.85cbakerycafe.com"
    start_urls = ["http://shoppersworldusa.com/store.html"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//div[@class="maincontent store"]//p/text()').extract()
        store_list = [tp.strip().replace('\n', '') for tp in store_list if tp.strip() != ""]
        for store in store_list:
            # try:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            if store.split(',')[0].strip()[0].isdigit() == False:
                item['store_name'] = store.split(',')[0].strip()
                item['address'] = store.split(',')[1].strip()
                item['city'] = store.split(',')[2].strip()
            else:
                item['store_name'] = ''
                item['address'] = store.split(',')[0].strip()
                item['city'] = store.split(',')[1].strip()
            
            address = item['address'] + ' ' + item['city']
            # if address.find('Pitkin Avenue') != -1:
            #     pdb.set_trace()
            location = geocoder.google(address)
            item['city'] = location.city
            item['state'] = location.state
            item['zip_code'] = location.postal
            item['address2'] = ''
            item['latitude'] = location.lat
            item['longitude'] = location.lng
            time.sleep(1)
            item['phone_number'] =  store.split(',')[-1].strip()

            item['store_hours'] = ''
            yield item
            # except:
            #     pdb.set_trace()

    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

