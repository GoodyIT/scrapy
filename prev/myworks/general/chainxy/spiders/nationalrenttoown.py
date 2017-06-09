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

class Nationalrenttoown(scrapy.Spider):
    name = "nationalrenttoown"

    domain = "https://nationalrto.com/"
    start_urls = ["https://nationalrto.com/locations"]
    phone_number = []

    def parse(self, response):
        store_list = response.xpath('.//div[contains(@class,"block")]')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_name'] = ''
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            phone =  self.validate(store.xpath('.//p[@class="phone"]/a/text()').extract_first())
            if phone in self.phone_number:
                continue
            else:
                self.phone_number.append(phone)
                item['phone_number'] = phone

            address = store.xpath('.//p[@class="address"]/text()').extract() 
            address = [tp.strip().replace('\n', '') for tp in address if tp.strip() != ""]
            _address = address[0] + ' ' + self.validate(store.xpath('.//p[@class="address"]/span/text()').extract_first())
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
            item['store_hours'] = ''
            hours = response.xpath('.//div[@class="hours"]/p')
            for hour in hours:
                item['store_hours'] += hour.xpath('.//span[1]/text()').extract_first() + ' ' + hour.xpath('.//span[2]/text()').extract_first() + '; '
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

