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

class Shopgarageonline(scrapy.Spider):
    name = "shopgarageonline"

    domain = "http://www.shopgarageonline.com"
    start_urls = ["http://www.garageclothing.com/us/json/storeLocationsJSON.jsp"]
    store_id = []

    def parse(self, response):
        pdb.set_trace()
        store_list = json.loads(response.body)
        for store in store_list:
            request = scrapy.Request(url= "http://www.garageclothing.com%s" % store, callback=self.parse_store)
            request.meta['store'] = store
            yield request

    def parse_content(self, response):
        store = response.meta['store']
        item = ChainItem()
        item['store_number'] = store['id']
        item['country'] = store['country']
        item['latitude'] = store['latitude']
        item['longitude'] = store['longitude']
        item['store_name'] = store['mallName']
        item['other_fields'] = ""
        item['coming_soon'] = "0"
        item['address'] = store['address1']
        item['address2'] = ''
        item['city'] = store['city']
        item['state'] = store['state']
        item['zip_code'] = store['postalCode']
        item['phone_number'] =  store['phoneNumber']

        hours = response.xpath('.//table[@class="storeHoursDetails]//tr')
        for hour in hours:
            item['store_hours'] = hour.xpath('.//td[1]/text()').extract_first() + ' ' + hour.xpath('.//td[2]/text()').extract_first() + "; "
      
        yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

