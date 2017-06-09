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

class Guthrieschicken(scrapy.Spider):
    name = "guthrieschicken"

    domain = "http://www.guthrieschicken.com/"
    start_urls = ["http://www.guthrieschicken.com/locations"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_list = response.xpath('.//div[@class="col-lg-2"]/p[2]')
        for store_info in store_list:
            item = ChainItem()
            info = store_info.xpath('.//text()').extract()

            item['store_number'] = ''
            item['store_name'] = self.validate(info[-4])
            item['city'] = self.validate(info[-2].split(',')[0])
            item['state'] = self.validate(info[-2].split(',')[1].strip().split(' ')[0])
            item['zip_code'] = self.validate(info[-2].split(',')[1].strip().split(' ')[1])
            item['address'] = self.validate(info[-3])
            item['address2'] = ''
            item['country'] = 'United States'
            item['phone_number'] = self.validate(info[-1].strip().encode('utf8').split('\xc2\xa0')[0])
            item['latitude'] = ''
            item['longitude'] = ''
            try:
                item['store_hours'] = self.validate(info[-1].strip().encode('utf8').split('\xc2\xa0')[-1].replace('Hours:', '').replace(',', ';'))
            except:
                item['store_hours'] = ''
            if item['store_hours'].find('(') != -1:
                item['store_hours'] = ''
            item['other_fields'] = ""
            item['coming_soon'] = "0"

            yield item


    def validate(self, value):
        if value != None:
            return value.strip().encode('utf8').replace('\xc2\xa0', '')
        else:
            return ""





        

