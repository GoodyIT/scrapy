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

class PeetsandteaSpider(scrapy.Spider):
    name = "peetsandtea"

    domain = "http://www.peets.com/"
    start_urls = ["http://www.peets.com/stores/peets-stores/stores-store-list.html"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_path = response.xpath('.//div[@class="storeItem"]')
        for store_info in store_path:
            item = ChainItem()
            store = store_info.xpath('.//text()').extract()
            
            try:
                item['store_number'] =  ''
                item['store_name'] = self.validate(store[0])
                # if item['address'].find('2121 H Street, NW, #131') != -1:
                citystatezip = self.parse_citystatezip(self.validate(store[2]))
                item['city'] = citystatezip[0]
                item['state'] = citystatezip[1]
                item['zip_code'] = citystatezip[2]
                item['address'] = self.validate(store[1])
                item['country'] = "United States"
                item['address2'] =  ''
                if len(store) == 4:
                    item['phone_number'] = ""
                else:
                    item['phone_number'] = self.validate(store[-2])
                item['latitude'] =  ''
                item['longitude'] = ''
                item['store_hours'] = self.validate(store[-1])
                item['other_fields'] = ""
                item['coming_soon'] = "0"    



                yield item
            except:
                pdb.set_trace()

    def validate(self, value):
        if value == None:
            return ""
        else:
            return value.strip().replace(u'\u2013', '-').replace(u'\u2014', '-')

    def parse_citystatezip(self, value):
        city = state = zip_code = ''
        if len(value.split(',')) == 3:
            city = self.validate(" ".join(value.split(',')[:-2]))
            state = self.validate(value.split(',')[-2])
            zip_code = self.validate(value.split(',')[-1])
        elif len(value.split(',')) == 2:
            city = self.validate(value.split(',')[0])
            state = self.validate(value.split(',')[1].strip().split(' ')[0])
            zip_code = self.validate(value.split(',')[1].strip().split(' ')[-1])
            if zip_code.find('90245') != -1:
                state = city.split(' ')[-1]
                city = " ".join(city.split(' ')[:-1])
        else:   
            city = self.validate(" ".join(value.split(' ')[:-2]))
            state = self.validate(value.split(' ')[-2])
            zip_code = self.validate(value.split(' ')[-1])
        return (city, state, zip_code)







        

