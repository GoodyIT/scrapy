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

import os, sys

import pdb

class Jackastorsbargrill(scrapy.Spider):
    name = "jackastorsbargrill"

    domain = "http://jackastors.com/wp-content/plugins/locations/script.php"
    start_urls = ["http://jackastors.com/wp-content/plugins/locations/script.php"]
    store_id = []

    def start_requests(self):
        yield FormRequest(url=self.start_urls[0], formdata={'page_size':'560','page':'1'}, headers={'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'*/*', 'Accept-Language':'en-US,en;q=0.8', 'X-Requested-With':'XMLHttpRequest'}, callback=self.parse_store) 

    def parse_store(self, response):
        store_list = response.xpath('//ul[@id="locations_table"]/li')
        for store in store_list:
            item = ChainItem()

            item['store_number'] = ''
            item['store_name'] = self.validate(store.xpath('.//h3/text()').extract_first().replace('-', ''))
            address = self.validate(store.xpath('.//div[@class="left"]/div/text()').extract_first())
            item['address'] = self.validate(address.split(',')[0])
            item['address2'] = ''
            
            item['city'] = self.validate(" ".join(address.split(',')[1].strip().split(' ')[:-1]))
            item['state'] = self.validate(address.split(',')[1].strip().split(' ')[-1])
            item['zip_code'] = ''
            if item['state'].find('NY') != -1:
                item['country'] = 'United States'
            else:
                item['country'] = 'Canada'
            item['phone_number'] = self.validate(store.xpath('.//div[@class="left"]/div/text()').extract()[1].replace('Telephone:', ''))
            hours = self.validate(store.xpath('.//div[@class="right"]/text()').extract_first())
            item['store_hours'] = self.validate("; ".join(hours).replace('Hours:', ''))
            item['coming_soon'] = "0"
            item['store_hours'] = ''
            item['latitude'] = ''
            item['longitude'] = ''
            item['other_fields'] = ''

            # if item['store_name'].find('Lansdowne Park') != -1:
            #     pdb.set_trace()
            
            yield item
   

    def validate(self, value):
        if value == None:
            return ""
        else:
            return value.encode('utf8').replace('\xc3\xa9', '').strip()




        

