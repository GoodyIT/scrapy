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

class Rockymountainchocolatefactory(scrapy.Spider):
    name = "rockymountainchocolatefactory"

    domain = "https://www.rmcf.com/"
    start_urls = ["http://www.rmcf.com/locations/"]
    store_id = []
    country_list = ["United States", "United Arab Emirates", "Canada", "Saudi Arabia"]

    def parse(self, response):
        store_list = response.xpath('.//tbody[@id="searchResults"]/tr')
        for store in store_list:
            item = ChainItem()
            item['country'] = store.xpath('.//td[4]/text()').extract_first().strip()
            if not item['country'] in self.country_list:
                continue

            item['store_number'] = ''
            item['latitude'] = store.xpath('.//@data-lat').extract_first()
            item['longitude'] = store.xpath('.//@data-lng').extract_first()
            item['zip_code'] = store.xpath('.//@data-zip').extract_first()
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['store_name'] = ''
            item['address'] = store.xpath('.//td[2]/text()').extract_first().strip()
            item['address2'] = ''
            item['city'] = store.xpath('.//td[1]/a/text()').extract_first()
            item['state'] = store.xpath('.//td[3]/text()').extract_first().strip()
            item['phone_number'] =  store.xpath('.//td[5]/a/text()').extract_first()

            item['store_hours'] = ''
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

