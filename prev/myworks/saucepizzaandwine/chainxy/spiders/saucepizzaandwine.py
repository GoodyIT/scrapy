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

class Saucepizzaandwine(scrapy.Spider):
    name = "saucepizzaandwine"

    domain = "http://www.saucepizzaandwine.com/"
    start_urls = ["http://www.saucepizzaandwine.com/"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_list = response.xpath('//div[@class="cont"]')
        for store_info in store_list:
            item = ChainItem()

            item['store_number'] = ''
            item['store_name'] = store_info.xpath('.//h3/a/text()').extract_first()
            item['city'] = store_info.xpath('.//div[@class="address"]/text()').extract()[2].strip().split(',')[0]
            item['state'] = " ".join(store_info.xpath('.//div[@class="address"]/text()').extract()[2].strip().split(',')[1].strip().split(' ')[:-1])
            item['zip_code'] = store_info.xpath('.//div[@class="address"]/text()').extract()[2].strip().split(',')[1].strip().split(' ')[-1]
            item['address'] = store_info.xpath('.//div[@class="address"]/text()').extract()[0].strip()
            item['address2'] = store_info.xpath('.//div[@class="address"]/text()').extract()[1].strip()
            item['country'] = 'United States'
            try:
                item['phone_number'] = store_info.xpath('.//div[@class="phone"]/text()').extract_first()
            except:
                item['phone_number'] = ''
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_hours'] = ""
            item['other_fields'] = ""
            item['coming_soon'] = "0"
                
            yield item

    def validate(self, value):
        if type(value) == "str":
            return value
        else:
            return ""





        

