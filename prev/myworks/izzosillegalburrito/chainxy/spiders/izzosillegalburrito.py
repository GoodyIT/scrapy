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
from lxml import etree

class Izzosillegalburrito(scrapy.Spider):
    name = "izzosillegalburrito"

    domain = "http://www.izzos.com/"
    start_urls = ["http://www.izzos.com/?q=store-locator/json"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.body)['features']
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store['properties']['nid']
            item['store_name'] = self.validate(store['properties']['name'])
            address = etree.HTML(store['properties']['description'])
            item['address'] = self.validate(address.xpath('.//div[@class="street-block"]/div/text()')[0])
            item['address2'] = ''
            item['country'] = 'United States'
            item['city'] = self.validate(address.xpath('.//span[@class="locality"]/text()')[0])
            item['state'] = self.validate(address.xpath('.//span[@class="state"]/text()')[0])
            try:
                item['zip_code'] = self.validate(address.xpath('.//span[@class="postal-code"]/text()')[0])
            except:
                item['zip_code'] = ''
            item['phone_number'] = self.validate(address.xpath('.//a/text()')[0])
            # if item['store_name'].find('17659 Glasgow Avenue') != -1:
            #     pdb.set_trace()
            item['latitude'] = store['geometry']['coordinates'][0]
            item['longitude'] = store['geometry']['coordinates'][1]
            hours = address.xpath('.//p/text()')[0].replace(u'\u2013', '-').split(',')
            item['store_hours'] = "; ".join(hours)
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            yield item

    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2013', '-').replace(u'\u2019', "'").replace('&#039;', '')
        else:
            return ""





        

