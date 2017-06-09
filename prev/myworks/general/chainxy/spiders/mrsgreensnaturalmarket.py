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

class Mrsgreensnaturalmarket(scrapy.Spider):
    name = "mrsgreensnaturalmarket"

    domain = "http://mrsgreens.com/"
    start_urls = ["http://mrsgreens.com/locations/"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//li[@class="table-row"]')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = store.xpath('.//@data-lat').extract_first()
            item['longitude'] = store.xpath('.//@data-lng').extract_first()
            item['store_name'] = self.validate(store.xpath('.//div/h4/a/text()').extract_first())
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            _address = store.xpath('.//p[@class="adr1"]/text()').extract_first() + ' ' + store.xpath('.//p[@class="adr2"]/text()').extract_first()
            addr = usaddress.parse(_address)
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
            item['phone_number'] =  self.validate(response.xpath('.//div[@class="adrBlock"]//strong/text()').extract_first())
            hours = response.xpath('.//div[@class="marketHour"]/p')
            item['store_hours'] = ''
            for hour in hours:
                item['store_hours'] += hour.xpath('.//strong/text()').extract_first() + ' ' + hour.xpath('.//em/text()').extract_first() + "; "
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

