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

class Frescas(scrapy.Spider):
    name = "frescas"

    domain = "http://www.frescas.com/"
    start_urls = ["http://www.frescas.com/locations/"]
    store_id = []

    def parse(self, response):
        store_list =  response.xpath("//script[contains(., 'var jsonContent =')]/text()").extract_first().split('var jsonContent =')[1].strip().split('console.log(jsonContent);')[0].strip().replace('{"data":', '')[:-2]
        for store in json.loads(store_list):
            item = ChainItem()
            item['store_number'] = store['id']
            item['country'] = 'United States'
            item['latitude'] = store['latitude']
            item['longitude'] = store['longitude']
            item['store_name'] = store['title']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store['street_number'] + ' ' + store['address_route']
            item['address2'] = ''
            item['city'] = store['city']
            item['state'] = store['state']
            item['zip_code'] = store['postal_code']
            item['phone_number'] =  store['phone']

            item['store_hours'] = store['hours'].replace('<dl class="lines">', '').replace(';', '').replace('\t', '').replace('</dl>', '').replace('</dt>', '').replace('<dd>', '').replace('</dd>', '; ').replace('<dt>', '').replace('\n', '').strip()
           
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

