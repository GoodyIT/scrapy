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

class Wyndhamhotelsandresorts(scrapy.Spider):
    name = "wyndhamhotelsandresorts"

    domain = "https://www.wyndhamhotels.com/"
    start_urls = ["https://www.wyndhamhotels.com/wyndham/our-locations"]
    phone_number = []
    def parse(self, response):
        state_list = response.xpath('.//div[@class="states-section__state col-md-8 col-sm-8 col-xs-24 mobile-fluid"]/a[1]/span/text()').extract()
        for state in state_list:
            if state.strip() != '':
                yield scrapy.Request(url="https://www.wyndhamhotels.com/BWSServices/services/search/searchByRegion?brand=wy&state=alaska%s" % state, callback=self.parse_store)
    
    def parse_store(self, response):
        pdb.set_trace()
        store_list = json.loads(response.body)['hostBrand']['availability']
        for store in store_list:
            item = ChainItem()
            item['phone_number'] =  store['tel']
            if store['tel'] in self.phone_number:
                continue
            self.phone_number.append(store['tel'])

            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = store['lat']
            item['longitude'] = store['lng']
            if len(store['name'].split('</b>')) == 2:
                item['store_name'] = store['name'].split('</b>')[1].strip()
            else:
                item['store_name'] = store['name']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store['address2']
            item['address2'] = store['address1']
            item['city'] = store['city']
            item['state'] = store['state']
            item['zip_code'] = store['zipCode']

            item['store_hours'] = ''
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

