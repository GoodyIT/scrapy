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
import usaddress

class Chuckdonspet(scrapy.Spider):
    name = "chuckdonspet"

    domain = "https://chuckanddons.com/"
    store_id = []

    def start_requests(self):
       yield FormRequest(url="https://chuckanddons.com/find-a-store/", formdata={"find-zip": "80104", "find-distance":"500", "find-state":"MN"}, callback=self.parse_store)

    def parse_store(self, response):
        store_list = response.xpath('.//div[@class="proximity-entry"]')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            hours = store.xpath('.//div[@class="store-hours"]/div')
            item['store_hours'] = ''
            for hour in hours:
                item['store_hours'] += hour.xpath('.//text()').extract_first() + hour.xpath('.//span/text()').extract_first() + "; "
            item['store_name'] = self.validate(store.xpath('.//div[@class="store-name"]/a/text()').extract_first())
            address = store.xpath('.//div[@class="store-address"]//text()').extract()
            address = [tp.strip() for tp in address if tp.strip() != ""]
            item['address'] = self.validate(address[0].split(',')[0].strip())
            if address[0].find(',') != -1:
                item['address2'] = self.validate(address[0].split(',')[1].strip())
                if self.hasNumbers(item['address2'][0]):
                    temp = item['address2']
                    item['address2'] = item['address'] 
                    item['address']  = temp

            citystatezip = self.parse_citystatezip(address[-1])
                
            item['country'] = 'United States'
            item['city'] = citystatezip[0]
            item['state'] =  "MN"
            item['zip_code'] =  citystatezip[2]
            item['phone_number'] =  store.xpath('.//div[@class="store-contact"]/div/span/text()').extract_first().replace('Tel:', '').strip()
            yield item
    
    def validate(self, value):
        if value != None:
            return value.replace('\n', '').replace(u'\u2013', '-').replace(u'\u2028', '').strip()
        else:
            return ""

    def parse_citystatezip(self, value):
        city = self.validate(value.split(',')[0])
        state = self.validate(value.split(',')[1].strip().split(' ')[0])
        zip_code = self.validate(value.split(',')[1].strip().split(' ')[-1])
        return (city, state, zip_code)

    def hasNumbers(self, inputString):
        return any(char.isdigit() for char in inputString)





        

