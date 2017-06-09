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

class Affordabledentures(scrapy.Spider):
    name = "affordabledentures"

    domain = "http://www.affordabledentures.com/"
    start_urls = ["http://www.affordabledentures.com/locations.xml?_=1495818430328"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//serviceArea')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store.xpath('.//@id').extract_first()
            item['country'] = 'United States'
            item['latitude'] = store.xpath('.//@lat').extract_first()
            item['longitude'] = store.xpath('.//@lng').extract_first()
            item['store_name'] = store.xpath('.//@name').extract_first()
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store.xpath('.//@address').extract_first()
            item['address2'] = ''
            item['city'] = store.xpath('.//@city').extract_first()
            item['state'] = store.xpath('.//@state').extract_first()
            item['zip_code'] = store.xpath('.//@zip').extract_first()
            item['phone_number'] =  store.xpath('.//@phone').extract_first()

            item['store_hours'] = ''
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

