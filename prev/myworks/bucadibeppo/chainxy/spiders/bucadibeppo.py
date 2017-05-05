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

class Bucadibeppo(scrapy.Spider):
    name = "bucadibeppo"

    domain = "http://www.bucadibeppo.com/"
    start_urls = ["http://www.bucadibeppo.com/restaurants/"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_list = response.xpath("//ul[@class='location-data']")
        for store_info in store_list:
            item = ChainItem()

            try:
                item['store_name'] = store_info.xpath(".//li[@class='location-name large-12 columns']/a/text()").extract_first().strip()
                item['store_number'] = ''
                address = store_info.xpath(".//li[@class='location-address large-4 columns']/text()").extract()
                item['address'] = address[0].strip()
                item['address2'] = ''
                if len(address) == 3:
                    item['address'] = address[0].strip() + " " + address[0].strip()
                    self.parse_address1(address[2].split(','), item)
                else:
                    self.parse_address1(address[1].split(','), item)
                    # item['city'] = address1.strip()
                    # item['state'] = address[1].split(',')[1].strip().split(" ")[0].strip()
                    # item['zip_code'] = address[1].split(',')[1].strip().split(" ")[2].strip()
                item['country'] = 'United States'
                try:
                    item['phone_number'] = store_info.xpath(".//li[@class='location-phone large-4 columns']/a/text()").extract_first().strip()
                except:
                    item['phone_number'] = ''
                item['latitude'] = ''
                item['longitude'] = ''

                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['store_hours'] = store_info.xpath(".//li[@class='location-phone large-4 columns']/text()").extract_first().strip()
            except:
                pdb.set_trace()  

            yield item
    def parse_address1(self, _address1, item):
        if len(_address1) == 3:
            item['city'] = _address1[0].strip()
            item['state'] = _address1[2].strip().split(" ")[0].strip()
            item['zip_code'] = _address1[2].strip().split(" ")[2].strip()
        else:
            item['city'] = _address1[0].strip()
            item['state'] = _address1[1].strip().split(" ")[0].strip()
            item['zip_code'] = _address1[1].strip().split(" ")[2].strip()





        

