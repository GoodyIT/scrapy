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

class Vipauto(scrapy.Spider):
    name = "vipauto"

    domain = "https://www.vipauto.com/"
    start_urls = ["https://www.vipauto.com/store-locator"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//table[@class="views-table cols-3"]/tbody/tr')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_name'] = store.xpath('.//td[1]/strong/text()').extract_first()
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store.xpath('.//td[1]//div[@class="street-address"]/text()').extract_first().strip()
            item['address2'] = ''
            item['city'] = store.xpath('.//td[1]//span[@class="locality"]/text()').extract_first().split(',')[0].strip()
            item['state'] = store.xpath('.//td[1]//span[@class="locality"]/text()').extract_first().split(',')[1].strip()
            item['zip_code'] = store.xpath('.//td[1]//span[@class="postal-code"]/text()').extract_first()
            item['phone_number'] =  store.xpath('.//td[2]/text()').extract_first().strip()

            item['store_hours'] = "; ".join(store.xpath('.//td[3]//ul/li/text()').extract())

            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

