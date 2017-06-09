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

class Biscuitscafe(scrapy.Spider):
    name = "biscuitscafe"

    domain = "http://biscuitscafe.com/"
    start_urls = ["http://biscuitscafe.com/locations/"]
    store_id = []

    def parse(self, response):
        pdb.set_trace()
        url_list = response.xpath('.//li[@id="menu-item-10577]/ul/li/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url= url, callback=self.parse_store)
        
    def parse_store(self, response):
        item = ChainItem()
        try:
            pdb.set_trace()
            item['store_number'] = ''
            item['store_name'] = response.xpath('.//h2/strong/text()').extract_first()
            address = response.xpath(".//div[@id='pageContent']/p[2]/text()").extract()
            addr = usaddress.parse(address)
            item['address'] = self.validate(store_info['address']['address1'])
            item['address2'] = self.validate(store_info['address']['address2'])
            item['city'] = self.validate(store_info['address']['city'])
            item['state'] = self.validate(store_info['address']['state'])
            item['zip_code'] = self.validate(store_info['address']['zip'])
            item['country'] = 'United States'
            item['phone_number'] = response.xpath('.//a[@class="bold mb2 db"]/text()').extract_first()
            item['latitude'] = ''
            item['longitude'] = ''
            
            item['store_hours'] = ''
            hours = response.xpath('.//div[@class="ph1 hours-wrap"]/div[@class="mb2"]/p')
            for hour in hours:
                item['store_hours'] += self.validate("".join(hour.xpath('.//text()').extract())) + "; "

            item['other_fields'] = ""
            item['coming_soon'] = "0"
            yield item
        except:
            pdb.set_trace()
                

    def validate(self, value):
        if value != None:
            return value.strip()
        else:
            return ""





        

