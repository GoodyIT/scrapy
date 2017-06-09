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

class Javau(scrapy.Spider):
    name = "javau"

    domain = "https://www.java-u.com/"
    start_urls = ["http://www.java-u.com/wp-admin/admin-ajax.php?action=store_search&lat=45.501689&lng=-73.56725599999999&max_results=25&radius=50&autoload=1"]
    store_id = []

    def start_requests(self):
        for x in xrange(1,3):
            if x == 1:
                yield scrapy.Request(url= self.start_urls[0], callback=self.parse_store)
            elif x == 2:
                yield scrapy.Request(url= "https://www.java-u.com/locations/", callback=self.parse_one)

    def parse_one(self, response):
        item = ChainItem()
            
        item['store_number'] = ''
        item['store_name'] = response.xpath('.//div[@id="text-block-17"]/p[1]/span/text()').extract_first()
        item['address'] = response.xpath('.//div[@id="text-block-17"]/p[2]/span[1]/text()').extract_first().replace(',', '')
        item['address2'] =  ''
        item['country'] = 'Canada'
        item['city'] = response.xpath('.//div[@id="text-block-17"]/p[2]/span[2]/text()').extract_first().split(',')[0]
        item['state'] =  response.xpath('.//div[@id="text-block-17"]/p[2]/span[2]/text()').extract_first().split(',')[1]
        item['zip_code'] =  ''
        item['phone_number'] = response.xpath('.//div[@id="text-block-17"]/p[2]/span[3]/text()').extract_first()
        item['latitude'] = ''
        item['longitude'] = ''
        item['store_hours'] = ''
        hours = response.xpath('.//div[@id="text-block-20"]/p/span/text()').extract()
        item['store_hours'] = self.validate('; '.join(hours))

        item['other_fields'] = ""
        item['coming_soon'] = "0"
        yield item

    def parse_store(self, response):
        store_list = json.loads(response.body)
        for store in store_list:
            item = ChainItem()
            
            item['store_number'] = store['id']
            item['store_name'] = self.validate(store['store'])
            item['address'] = self.validate(store['address'])
            item['address2'] =  self.validate(store['address'])
            item['country'] = 'Canada'
            item['city'] = self.validate(store['city'])
            item['state'] =  self.validate(store['state'])
            item['zip_code'] =  self.validate(store['zip'])
            item['phone_number'] = self.validate(store['phone'])
            item['latitude'] = self.validate(store['lat'])
            item['longitude'] = self.validate(store['lng'])
            item['store_hours'] = ''
            try:
                hours =  html.fromstring(store['hours'])
                for hour in hours:
                    item['store_hours'] += " ".join(hour.xpath('.//text()')) + "; "
            except:
                item['store_hours'] = ''

            item['other_fields'] = ""
            item['coming_soon'] = "0"
            yield item

    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2013', '-').replace(u'\u2019', "'").replace('&#039;', '').encode('utf8').replace('\xc3\xb4', 'o').replace('\xc3\xa9', 'e')
        else:
            return ""





        

