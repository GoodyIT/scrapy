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

class Seescandies(scrapy.Spider):
    name = "seescandies"

    domain = "http://www.sees.com"
    start_urls = ["http://maps.sees.com/api/getAsyncLocations?template=search&level=search&radius=10000000000&search=US%2C+73118"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.body)['markers']
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store['locationId']
            if store['locationId'] in self.store_id:
                continue
            self.store_id.append(store['locationId'])
            
            item['country'] = 'United States'
            item['latitude'] = store['lat']
            item['longitude'] = store['lng']
            info = html.fromstring(store['info'])
            item['store_name'] = self.validate(info.xpath('.//div[@class="indy_popup_addr"]/div[1]/a/text()'))
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = self.validate(info.xpath('.//div[@class="indy_popup_addr"]/div[2]/text()'))
            item['address2'] = self.validate(info.xpath('.//div[@class="indy_popup_addr"]/div[3]/text()'))
            parse_citystatezip = self.parse_citystatezip(self.validate(info.xpath('.//div[@class="indy_popup_addr"]/div[4]/text()')))
            item['city'] = parse_citystatezip[0]
            item['state'] = parse_citystatezip[1]
            item['zip_code'] = parse_citystatezip[2]
            item['phone_number'] =  self.validate(info.xpath('.//div[@class="indy_popup_addr"]/div[5]/text()')).replace('Ph:', '').strip()

            item['store_hours'] = "; ".join(info.xpath('.//meta[@itemprop="openingHours"]/@content'))
            yield item
    
    def validate(self, value):
        if len(value) > 0:
            return value[0]
        else:
            return ""

    def parse_citystatezip(self, value):
        if value == '':
            return ('', '', '')
        city = value.split(',')[0].strip()
        state = value.split(',')[1].strip().split(' ')[0].strip()
        zip_code = value.split(',')[1].strip().split(' ')[-1].strip()
        return (city, state, zip_code)





        

