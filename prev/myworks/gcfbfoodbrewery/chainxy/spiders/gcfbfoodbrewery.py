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

class Gcfbfoodbrewery(scrapy.Spider):
    name = "gcfbfoodbrewery"

    domain = "http://www.gcfb.com/"
    start_urls = ["http://www.gcfb.com/locations/"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        url_list = response.xpath('.//select[@name="Location Select"]/option/@value').extract()
        for url in url_list:
            request = scrapy.Request(url='http://www.gcfb.com/locations/?l=%s' % url, callback=self.parse_store)
            yield request
    def parse_store(self, response):
        store_list = response.xpath('.//div[@class="locationShortDetails"]')
        for store in store_list:
            request = scrapy.Request(url=store.xpath('.//h3/a/@href').extract_first(), callback=self.parse_hours)
            request.meta['store_name'] = store.xpath('.//h3/a/text()').extract_first().strip()
            info = store.xpath('.//p[@class="locationListAddr"]/text()').extract()
            request.meta['address'] = info[0]
            request.meta['city'] = info[1].split(',')[0].strip()
            request.meta['state'] = "".join(info[1].split(',')[1].strip().split(' ')[:-1]).strip()
            request.meta['zip_code'] = info[1].split(',')[1].strip().split(' ')[-1].strip()
            request.meta['phone_number'] = info[2]
            yield request

    def parse_hours(self, response):
        item = ChainItem()

        item['store_number'] = ''
        item['store_name'] = response.meta['store_name']
        item['city'] = response.meta['city']
        item['state'] = response.meta['state']
        item['zip_code'] = response.meta['zip_code']
        item['address'] = response.meta['address']
        item['address2'] = ''
        item['latitude'] = ''
        item['longitude'] = ''
        item['country'] = 'United States'
        item['phone_number'] = response.meta['phone_number']
        hours = response.xpath('.//div[@class="sideBarMod"]/ul')
        item['store_hours'] = ''
        for hour in hours:
            item['store_hours'] += "".join(hour.xpath('.//li/text()').extract()) + "; "
        
        item['store_hours'] = item['store_hours'].replace(u'\u2013', '-')
        item['other_fields'] = ""
        item['coming_soon'] = "0"

        yield item

    def validate(self, value):
        if value != None:
            return value.strip()
        else:
            return ""





        

