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

class Doscoyotesborder(scrapy.Spider):
    name = "doscoyotesborder"

    domain = "http://doscoyotes.com/"
    start_urls = ["http://doscoyotes.com/locations/"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('//article[@class="location-listing"]')
        for store in store_list:
            item = ChainItem()
            address = store.xpath('.//section[@class="location-address"]/p/text()').extract()
            addr = usaddress.parse(" ".join(address))
            city = state = zip_code = address = ''
            for temp in addr:
                if temp[1] == 'PlaceName':
                    city += temp[0].replace(',','') + ' '
                elif temp[1] == 'StateName':
                    state = temp[0].replace(',','')
                elif temp[1] == 'ZipCode':
                    zip_code = temp[0].replace(',','')
                else:
                    address += temp[0].replace(',','') + ' '
            
            item['address'] = address
            item['city'] = city
            item['state'] =  state
            item['zip_code'] =  zip_code
            item['store_number'] = store.xpath('.//@id').extract_first().replace('location-', '')
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['store_hours'] = ''
            item['store_name'] = store.xpath('.//header/h2/text()').extract_first()
            item['address2'] = ''
            item['phone_number'] =  store.xpath('.//section[@class="location-phone"]/p/text()').extract_first().replace('Phone:', '').strip()
            
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

