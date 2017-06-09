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

class Samuelsjewelers(scrapy.Spider):
    name = "samuelsjewelers"

    domain = "https://samuelsjewelers.com"
    start_urls = [""]
    store_id = []

    headers = {
        "Accept":"text/javascript, text/html, application/xml, text/xml, */*",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"
    }

    def __init__(self):
        states   = open('states.json', 'rb')
        self.states = json.loads(states.read())
    def start_requests(self):
        request_url = "http://www.samuelsjewelers.com/ustorelocator/location/searchJson/"
        for state in self.states:
            form_data = {
                'radius':'20000',
                'lat':str(state['latitude']),
                'lng':str(state['longitude'])
            }
            yield FormRequest(url=request_url, formdata=form_data, headers=self.headers, callback=self.parse_url)

    def parse_url(self, response):
        store_list = json.loads(response.body)['markers']
        for store in store_list:
            try:
                request = scrapy.Request(url= "https://samuelsjewelers.com" + store['custom_data']['custom2'].split('href=')[1].split('><font')[0].strip(), callback=self.parse_store)
                request.meta['store'] = store
            except:
                self.parse_content(store)
            yield request

    def parse_content(self, store):
        item = ChainItem()
        if store['store_id'] in self.store_id:
            return
        self.store_id.append(store['store_id'])
        item['store_number'] = store['store_id']

        item['country'] = 'United States'
        item['latitude'] = store['latitude']
        item['longitude'] = store['longitude']
        item['store_name'] = store['title']
        item['other_fields'] = ""
        item['coming_soon'] = "0"
        item['address'] = store['address'].split(',')[0]
        item['address2'] = ''
        item['city'] = store['city']
        item['state'] = store['state']
        item['zip_code'] = store['zipcode']
        item['phone_number'] =  store['phone']

        item['store_hours'] = "; ".join(hours[3:]).strip()
        yield item

    def parse_store(self, response):
        store = response.meta['store']
        item = ChainItem()
        item['store_number'] = store['store_id']
        item['country'] = 'United States'
        item['latitude'] = store['latitude']
        item['longitude'] = store['longitude']
        item['store_name'] = store['title']
        item['other_fields'] = ""
        item['coming_soon'] = "0"
        item['address'] = store['address'].split(',')[0]
        item['address2'] = ''
        item['city'] = store['city']
        item['state'] = store['state']
        item['zip_code'] = store['zipcode']
        item['phone_number'] =  store['phone']

        hours = response.xpath('.//table//tr[1]/td[2]/text()').extract()
        item['store_hours'] = "; ".join(hours[3:]).strip()
        yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

