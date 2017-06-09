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

class Wholesalesports(scrapy.Spider):
    name = "wholesalesports"

    domain = "http://www.wholesalesports.com/"
    start_urls = ["http://www.wholesalesports.com/store/wsoo/en/store-finder"]
    store_id = []

    def parse(self, response):
        pdb.set_trace()
        store_list = json.loads(response.xpath('.//div[@id="map_canvas"]/@data-stores').extract_first())
        idxs = []
        for idx in store_list:
            idxs.append(idx)

        for idx in idxs:
            store = store_list[idx]
            item = ChainItem()
            item['store_number'] = store['id']
            item['country'] = 'United States'
            item['latitude'] = store['latitude']
            item['longitude'] = store['longitude']
            item['store_name'] = store['name']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            details = html.fromstring(store['details'])
            item['address'] = store['address']
            item['address2'] = store['address2']
            item['city'] = store['city']
            item['state'] = store['state']
            item['zip_code'] = store['zip']
            item['phone_number'] =  store['phone']

            item['store_hours'] = store['description'].replace('<p>', '').replace('</p>', '').replace('<br />', '').replace('&#8211;', '-').replace('\n', '; ').replace('<span>', '').replace('</span>', '').replace('<b>', '').replace('</b>', '').replace('<!--; <p class="p1">', '').replace('Soft Opening Hours 10AM - 8PM daily until Dec. 29; ; -->', '').strip()
      
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

