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
import usaddress

class Wolffurniture(scrapy.Spider):
    name = "wolffurniture"

    domain = "http://www.wolffurniture.com/"
    start_urls = ["http://www.wolffurniture.com/stores"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//div/address')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store.xpath('.//@data-store-number').extract_first()
            item['country'] = 'United States'
            item['latitude'] = store.xpath('.//@data-latitude').extract_first()
            item['longitude'] = store.xpath('.//@data-longitude').extract_first()
            item['store_name'] = store.xpath('.//@data-name').extract_first()
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address2'] = ''
            address = store.xpath('.//@data-address').extract_first()
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
            item['phone_number'] =  store.xpath('.//span[@class="phone"]/text()').extract_first()

            hours = store.xpath('.//div[@class="hours"]/table//tr')
            item['store_hours'] = ''
            for hour in hours:
                item['store_hours'] += hour.xpath('.//th/text()').extract_first() + ' ' + hour.xpath('.//td/text()').extract_first() + '; '
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

