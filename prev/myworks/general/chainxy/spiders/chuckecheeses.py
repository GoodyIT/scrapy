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

class Chuckecheeses(scrapy.Spider):
    name = "chuckecheeses"

    domain = "https://www.chuckecheese.com/"
    start_urls = ["https://www.chuckecheese.com/locations/?type=5&val=41.9577761;-87.6556468&miles=100000"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.xpath("//script[contains(., 'var CECLocations =')]/text()").extract_first().split('var CECLocations = {')[1].split('var currentzip = 40100;')[0].replace('\r\n', '').strip().split('"Locations":')[1].split('};')[0])
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store['id']
            item['latitude'] = store['lat']
            item['longitude'] = store['lng']
            item['store_name'] = store['name']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store['address']
            item['address2'] = ''
            item['city'] = store['city']
            item['state'] = store['state']
            item['zip_code'] = self.validate(store['postal'])
            if self.validate(store['postal']) == '' or store['state'] == '' or len(store['state'])> 2:
                continue
            elif self.validate(store['postal'])[0].isdigit():
                item['country'] = 'United States'
            else:
                item['country'] = 'Canada'

            item['phone_number'] =  store['phone']
            item['store_hours'] = ''
            if self.validate(store['hours']) != '':
                hours =  html.fromstring(store['hours']).xpath('.//time/text()')
                item['store_hours'] = '; '.join(hours)
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

