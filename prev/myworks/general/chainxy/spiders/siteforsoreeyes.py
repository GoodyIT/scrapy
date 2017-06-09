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

class Siteforsoreeyes(scrapy.Spider):
    name = "siteforsoreeyes"

    domain = "http://www.siteforsoreeyes.com/"
    start_urls = ["http://www.siteforsoreeyes.com/locations/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//a[@class="link-emphasis single-location-link"]/@href').extract()
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse_store)

    def parse_store(self, response):
        item = ChainItem()
        item['store_number'] = ''
        item['country'] = 'United States'
        item['latitude'] = ''
        item['longitude'] = ''
        item['store_name'] = response.xpath('.//a[@class="location-page-link-city"]/text()').extract_first().strip()
        item['other_fields'] = ""
        item['coming_soon'] = "0"
        item['address'] = self.validate(response.xpath('.//span[@class="street-address"]/text()').extract_first())
        item['address2'] = ''
        item['city'] = response.xpath('.//span[@class="locality"]/text()').extract_first().strip()
        item['state'] = response.xpath('.//span[@class="region"]/text()').extract_first().strip()
        item['zip_code'] = response.xpath('.//span[@class="postal-code"]/text()').extract_first().strip()
        item['phone_number'] =  response.xpath('.//a[@class="tel"]/text()').extract_first().strip()

        hours = response.xpath('.//ul[@class="location-hours-list store-hours"]/li/text()').extract()
        item['store_hours'] = '; '.join(hours)
        yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-').replace(u'\u2013', '-')
        else:
            return ""





        

