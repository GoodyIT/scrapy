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

class Roomboard(scrapy.Spider):
    name = "roomboard"

    domain = "http://www.roomandboard.com/"
    start_urls = ["http://www.roomandboard.com/more_ways_to_shop/stores/store_locations.ftl"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//div[@class="store clearfix"]')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_name'] = store.xpath('.//h4/a[1]/text()').extract_first()
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address2'] = ''
            address = store.xpath('.//ul[@class="addr"]/li[1]/text()').extract_first() + ' ' + store.xpath('.//ul[@class="addr"]/li[2]/text()').extract_first()
            addr = usaddress.parse(address)
            city = state = zip_code = street = ''
            for temp in addr:
                if temp[1] == 'PlaceName':
                    city += temp[0].replace(',','') + ' '
                elif temp[1] == 'StateName':
                    state = temp[0].replace(',','')
                elif temp[1] == 'ZipCode':
                    zip_code = temp[0].replace(',','')
                else:
                    street += temp[0].replace(',','') + ' '
            # pdb.set_trace()
            item['address'] = street
            item['city'] = city
            item['state'] =  state
            item['zip_code'] =  zip_code
            item['phone_number'] =  store.xpath('.//ul[@class="addr"]/li[3]/text()').extract_first()

            hours = store.xpath('.//ul[@class="hours"]/li')
            item['store_hours'] = ''
            for hour in hours:
                item['store_hours'] += self.validate(hour.xpath('.//span[1]/text()').extract_first()) + ' ' + self.validate(hour.xpath('.//span[2]/text()').extract_first()) + '; '
            
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

