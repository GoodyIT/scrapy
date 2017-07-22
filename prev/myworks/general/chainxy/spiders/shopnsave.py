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

class Shopnsave(scrapy.Spider):
    name = "shopnsave"

    domain = "https://www.shopnsave.com/"
    start_urls = ["https://www.shopnsave.com/stores/search-stores.html"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//div[@id="find-view-states"]//li/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url= "https://www.shopnsave.com" + url + "&maxResults=50&zipCode=&city=&lat=&long=&radius=10&address1=", callback=self.parse_store)
    
    def parse_store(self, response):
        store_list = response.xpath('.//table[@id="store-search-result"]/tbody/tr')
        try:
            for x in range(0, len(store_list)-2):
                store = store_list[x+1]
                if not store:
                    continue
                if store.xpath('.//td/@colspan').extract_first() == '4':
                    continue
                item = ChainItem()
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                address = store.xpath('.//td[@class="store-result-address"]/text()').extract()
                address = [tp.strip().replace('\n', '') for tp in address if tp.replace('\n', '').strip() != ""]
                item['store_hours'] = address[-1]
                item['store_name'] = address[0]
                item['address'] = address[1]
                item['address2'] = ''
                item['store_number'] = address[0].split('-')[0].strip().split(' ')[-1]
                citystatezip = self.parse_citystatezip(address[2])
                item['city'] = citystatezip[0]
                item['state'] = citystatezip[1]
                item['zip_code'] = citystatezip[2]
                try:
                    item['phone_number'] =  store.xpath('.//td[@class="store-result-phone"]/text()').extract_first().split(u'\u2014')[0].strip()
                except:
                    item['phone_number'] =  ''

                yield item
        except:
            pdb.set_trace()
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""

    def parse_citystatezip(self, value):
        city = self.validate(value.split(',')[0])
        state = self.validate(value.split(',')[1].strip().split(u'\xa0')[0])
        zip_code = self.validate(value.split(',')[1].strip().split(u'\xa0')[-1])
        return (city, state, zip_code)





        

