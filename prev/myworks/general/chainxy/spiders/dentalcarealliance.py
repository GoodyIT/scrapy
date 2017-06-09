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

class Dentalcarealliance(scrapy.Spider):
    name = "dentalcarealliance"

    domain = "http://www.dentalcarealliance.net/"
    start_urls = ["http://www.dentalcarealliance.net/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//select[@name="header_state"]/option/@value').extract()
        for url in url_list:
            if url.strip() != '':
                if url[-1] == '/':
                    yield scrapy.Request(url="http://www.dentalcarealliance.net/affiliated-practices/" + url, callback=self.parse_store)
                else:
                    yield scrapy.Request(url="http://www.dentalcarealliance.net/affiliated-practices/" + url + '/', callback=self.parse_store)
             
    def parse_store(self, response):
        store_list = response.xpath('.//ul[@class="locations_list no_bullets"]/li')
        for store in store_list:
            try:
                item = ChainItem()
                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['store_name'] = self.validate(store.xpath('.//a[@class="location_name"]/text()').extract_first())
                address = store.xpath('.//div[@class="address"]/text()').extract()
                address = [tp.strip() for tp in address if tp.strip() != ""]
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
                item['country'] = 'United States'
                item['city'] = city
                item['state'] =  state
                item['zip_code'] =  zip_code
                item['address2'] = ''
                item['phone_number'] = self.validate(store.xpath('.//div[@class="phone"]/text()').extract_first())
                item['store_hours'] = ''
               
                yield item
            except:
                pdb.set_trace()
            
    def validate(self, value):
        if value != None:
            return value.replace(u'\u2019', '-').replace(u'\u2013', '-').replace('Phone:', '').strip()
        else:
            return ""





        

