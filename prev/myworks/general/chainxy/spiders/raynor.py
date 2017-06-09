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

class Raynor(scrapy.Spider):
    name = "raynor"

    domain = "http://www.raynor.com/"
    start_urls = ["http://www.raynor.com/ListDealersGoogle.cfm"]
    store_id = []

    def __init__(self):
        ca_json = open('citiesusca.json', 'rb')
        self.ca_long_lat_fp = json.load(ca_json)

    def start_requests(self):
        for city in self.ca_long_lat_fp:
            formdata = {
                "type":"Radius",
                "zip5":self.ca_long_lat_fp[city]["zip_code"],
                "searchzip": "Search",
                "lat":"0",
                "lon":"0"
            }
            headers = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Content-Type":"application/x-www-form-urlencoded"
            }
            yield FormRequest(url=self.start_urls[0], headers=headers, formdata=formdata, callback=self.parse_store)

    def parse_store(self, response):
        store_list = json.loads(response.body)
        for store in store_list:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_name'] = store.xpath('.//strong/text()').extract_first()
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            address = store.xpath('./text()').extract()
            address = [tp.strip().replace('\n', '') for tp in address if tp.strip() != ""][1:-1]
            addr = usaddress.parse(" ".join(address[:-1]))
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
            item['phone_number'] = address[-1]

            item['store_hours'] = ''
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

