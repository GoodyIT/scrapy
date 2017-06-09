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

class Davesmarkets(scrapy.Spider):
    name = "davesmarkets"

    domain = "http://www.davesmarkets.com/"
    start_urls = ["http://www.davesmarkets.com/locations.shtml"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//tr[@class="lucida14"]//text()').extract()
        store_list = [tp.strip().replace('\n', '').replace('\r', '') for tp in store_list if tp.strip() != ""]
        # pdb.set_trace()
        request = scrapy.Request(url=self.domain, callback=self.parse_body)
        request.meta['store_list'] = store_list
        yield request

    def parse_body(self, response):
        store_list = response.meta['store_list']
        store = []
        _first = store_list[0]
        for x, value in enumerate(store_list[1:]):
            if value.find('(Click here for directions)') != -1:
                if len(store) > 1:
                    # pdb.set_trace()
                    # parse store
                    _first = store[-1]
                    store = store[:-1]
                    result = self.myfunc(store)
                    store = []
                    yield result
                else:
                    continue
            else:
                # if _first.find('WILSON MILLS') != -1:
                #     pdb.set_trace()
                if _first.strip() != '':
                    store.append(_first)
                    _first = ''
                store.append(value)
                if x == len(store_list[1:])-1:
                    result = self.myfunc(store)
                    store = []
                    yield result

    def myfunc(self, response):
        store = response
        item = ChainItem()
        item['store_name'] = store[0].replace('-', '').strip()
        item['store_number'] = ''
        item['country'] = 'United States'
        item['latitude'] = ''
        item['longitude'] = ''
        item['other_fields'] = ""
        item['coming_soon'] = "0"
        item['address'] = store[1].split(',')[0].strip()
        item['city'] = store[1].split(',')[1].strip()
        item['state'] =  ''
        item['zip_code'] =  store[1].split(',')[2].strip()
        item['phone_number'] =  store[3]
        hours = []
        isHour = False
        for hour in store[4:]:
            if hour == 'Hours:':
               isHour = True
               continue
            elif isHour:
                # pdb.set_trace()
                if hour.find('Hours:') != -1:
                    break
                hours.append(hour)
            else:
                continue

        item['store_hours'] = ''
        for x, hour in enumerate(hours):
            if x >= 1 and x % 2 == 1:
                continue
            else:
                item['store_hours'] += hour + ':' + hours[x+1] + "; " 

        store = []
        return item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""
