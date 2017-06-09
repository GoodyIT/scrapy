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

class Miamisubs(scrapy.Spider):
    name = "miamisubs"

    domain = "http://miamisubs.com/"
    start_urls = ["http://miamisubs.com/locations"]
    store_id = []

    def parse(self, response):
        containers = response.xpath('.//div[@class="addressContainer"]/a')
        for store in containers:
            item = ChainItem()

            item['store_number'] = ''
            item['store_name'] = store.xpath('.//div[@class="address"]//p/text()').extract_first()
            if item['store_name'] == None:
                item['store_name'] = ''

            # loc = store.xpath('.//@href').extract_first().split('ll=')
            # if len(loc) == 1:
            #     loc = store.xpath('.//@href').extract_first().split('/@')
            # if len(loc) != 1:
            #     loc = loc[1].strip().split(',')
            #     item['latitude'] = loc[0]
            #     item['longitude'] = loc[1]
                
            item['address2'] = ''
            item['city'] = ''
            item['state'] = ''
            item['zip_code'] = ''
            item['country'] = ''
            item['coming_soon'] = "0"
            item['store_hours'] = ''

            citystatezip = store.xpath('.//div[@class="address"]/h4[1]/text()').extract_first()
            if citystatezip.find('Malaysia') != -1:
                item['city'] = citystatezip.split(',')[0].strip()
                item['country'] = 'Malaysia'
            elif citystatezip.find('Panama') != -1:
                item['country'] = 'Panama'
            elif citystatezip.find('Myanmar') != -1:
                item['country'] = 'Myanmar'
                item['city'] = citystatezip.split(',')[0].strip()
            else:
                item['city'] = citystatezip.split(',')[0].strip()
                if item['store_name'].find('Relocating. Check back soon!') != -1:
                    item['phone_number'] = ''
                elif item['city'].find('Coming Soon') != -1:
                    item['phone_number'] = ''
                    item['coming_soon'] = "1"
                    citystatezip = store.xpath('.//div[@class="address"]/h4[2]/text()').extract_first()
                else:
                    try:
                        item['phone_number'] = store.xpath('//div[@class="address"]//h4[2]/text()').extract_first()
                    except:
                        item['phone_number'] = ''
                if len(citystatezip.split(',')) == 1:
                    item['city'] = ''
                    item['state'] = citystatezip
                    item['zip_code'] = ''
                else:
                    item['state'] = citystatezip.split(',')[1].strip().split(' ')[0]
                    try:
                        item['zip_code'] = citystatezip.split(',')[1].strip().split(' ')[1]
                    except:
                        item['zip_code'] = ''
                item['address'] = item['store_name']
                item['country'] = 'United States'

            item['other_fields'] = self.validate(response.xpath('.//div[@class="address"]//div[@class="features"]//p/text()').extract_first())
            
            if item['store_name'].find('Check back soon!') != -1:
                item['coming_soon'] = "1"

            hours = store.xpath('.//div[@class="features"]/p/text()').extract_first()
            if hours != None and hours.find('Open 24 hrs') != -1:
                item['store_hours'] = 'Open 24 hrs'
                
            yield item
   

    def validate(self, value):
        if value == None:
            return ""
        else:
            return value




        

