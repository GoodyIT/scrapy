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
from lxml import html

class akinsnaturalfoodmarket(scrapy.Spider):
    name = "akinsnaturalfoodmarket"

    domain = "http://www.akins.com/"
    start_urls = ["http://www.akins.com/retailer/store_templates/am_custom_page.asp?PageID=1286&storeID=A59A6B1C10E44C9E9420A7A75B27460A"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//div[@id="topCentralBlock"]//text()').extract()
        store_list = [tp.strip().replace('\n', '').replace('\r', '') for tp in store_list if tp.strip() != ""]
        
        request = scrapy.Request(url=self.domain, callback=self.parse_body)
        request.meta['store_list'] = store_list
        yield request
        
            
    def parse_body(self, response):
        store = []
        for value in response.meta['store_list']:
            if value.find('Click here to get directions') != -1:
                item = ChainItem()
                item['store_name'] = ''
                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['address2'] = ''
                getName = False
                getAddress = False
                address = ''
                for x, _value1 in enumerate(store):
                    if _value1.find('Phone') != -1:
                        getAddress = True
                        if item['store_name'].find('Fremont Shopping Center') != -1:
                            pdb.set_trace()
                        if address.find(')') != -1:
                            address = address.split(')')[1]
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
                        item['phone_number'] =  _value1.replace('Phone:', '').strip()
                        if store[x+1].split('-')[0].isdigit() == True:
                            item['store_hours'] = self.validate(" ".join(store[x+2:]))
                            item['phone_number'] += ' ' + store[x+1]
                        else:
                            item['store_hours'] = self.validate(" ".join(store[x+1:]))
                    elif _value1.split(' ')[-1].find('Center') != -1 or _value1.split(' ')[-1].find('Marketplace') != -1 or _value1.find('Newport Square') != -1:
                        item['store_name'] += _value1
                        getName = True
                    elif getName == False and getAddress == False:
                        item['store_name'] += _value1 + ' '
                    elif getName == True and getAddress == False:
                        address += _value1 + ' '

                yield item
                store = []
            else:
                store.append(value) 
    
    def validate(self, value):
        if value != None:
            return value.strip().encode('utf8').replace('\xc2\xa0', '')
        else:
            return ""





        

