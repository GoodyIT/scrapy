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

class Choicepet(scrapy.Spider):
    name = "choicepet"

    domain = "http://www.choicepet.com"
    start_urls = ["http://www.choicepet.com/locations/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//div[@class="location wpb_column vc_column_container vc_col-sm-4"]//a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse_store)
        
    def parse_store(self, response):
        store_list = response.xpath('.//div[@class="content content-location row"]')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_name'] = self.validate(store.xpath('.//div[@class="address col-sm-3"]/p[@class="title"]/a/text()').extract_first())
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            _address = store.xpath('.//div[@class="address col-sm-3"]/p[@class="address"]/text()').extract()
            _address = [tp.strip().replace('\n', '') for tp in _address if tp.strip() != ""]
            addr = usaddress.parse(" ".join(_address))
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
            item['address'] = street
            item['city'] = city
            item['state'] =  state
            item['zip_code'] =  zip_code
            item['address'] = street
            item['address2'] = ''
            item['phone_number'] =  self.validate(store.xpath('.//div[@class="address col-sm-3"]/p[@class="phone"]/text()').extract_first())
            hours = store.xpath('.//div[@class="address col-sm-3"]/p[@class="hours"]/text()').extract()
            hours = [tp.strip().replace('\n', '') for tp in hours if tp.strip() != ""]
            item['store_hours'] = self.validate('; '.join(hours))
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-').replace(u'\u2013', '-')
        else:
            return ""





        

