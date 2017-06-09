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

class Raleys(scrapy.Spider):
    name = "raleys"

    domain = "https://www.raleys.com/"
    start_urls = ["https://www.raleys.com/www/storelocator"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//table[@width="900"]')[2].xpath('.//tr/td')
        for store in store_list[1:-1]:
            try:
                item = ChainItem()
                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                item['store_name'] = store.xpath('.//a/b/text()').extract_first()
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                address = store.xpath('.//a/text()').extract()[1][1:].strip()
                addr = usaddress.parse(address)
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
                item['phone_number'] = store.xpath('./text()').extract()[1].split('|')[1]
                hours = ''.join(store.xpath('./text()').extract()[1].split('|')[2].split(':')[1:]).strip()
                idx = 0
                for x, hour in enumerate(hours):
                    if hour.isdigit():
                        idx = x
                        break
                item['store_hours'] = hours[x:]
                yield item
            except:
                pdb.set_trace()
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

