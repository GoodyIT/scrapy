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

class Intelligentsiacoffee(scrapy.Spider):
    name = "intelligentsiacoffee"

    domain = "https://www.intelligentsiacoffee.com/locations"
    start_urls = ["https://www.intelligentsiacoffee.com/locations"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//div[@class="row"]/div[contains(@class, "col-md-6")]')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = ''
            item['store_name'] = self.validate(store.xpath('.//h3/a/text()').extract_first())
            if item['store_name'] == '':
                continue
            address = store.xpath('.//div[@class="block-text block-text-left"]/p/text()').extract()
            address = [tp.strip() for tp in address if tp.strip() != ""]
            item['address'] = self.validate(address[0])
            item['country'] = 'United States'
            if len(address) == 2:
                item['city'] = self.validate(address[1].split(',')[0])
                item['state'] =  self.validate(" ".join(address[1].split(',')[1].strip().split(' ')[:-1]))
                item['zip_code'] =  self.validate(address[1].split(',')[1].strip().split(' ')[-1])
                item['phone_number'] = ''
            else:
                if len(address) == 4:
                    item['address2'] =  self.validate(address[1])
                else:
                    item['address2'] =  ''
                    
                item['city'] = self.validate(address[-2].split(',')[0])
                item['state'] =  self.validate(" ".join(address[-2].split(',')[1].strip().split(' ')[:-1]))
                item['zip_code'] =  self.validate(address[-2].split(',')[1].strip().split(' ')[-1])
                item['phone_number'] = self.validate(address[-1])

            item['latitude'] = ''
            item['longitude'] = ''
            item['store_hours'] = ''
            hours = store.xpath('.//div[@class="block-text block-text-right"]/p[1]/text()').extract()
            item['store_hours'] = ""
            try:
                for hour in hours:
                    item['store_hours'] += hour.split('/')[1].strip() + ':' +  hour.split('/')[0].strip() + "; "
            except:
                item['store_hours'] = hours[0]

            if item['store_hours'].find('By Appointment Only') != -1 or item['store_hours'].find('Coming Spring 2017') != -1:
                item['store_hours'] = ''
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            yield item
       

    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2013', '-').replace(u'\u2019', "'").replace('&#039;', '')
        else:
            return ""





        

