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
import usaddress

class Choicesmarketscanada(scrapy.Spider):
    name = "choicesmarketscanada"

    domain = "https://www.choicesmarkets.com/"
    start_urls = ["https://www.choicesmarkets.com/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//ul[@class="locations-sub-menu"]/li/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url= url, callback=self.parse_store)
    
    def parse_store(self, response):
        item = ChainItem()
        item['store_number'] = ''
        item['country'] = 'Canada'
        item['latitude'] = ''
        item['longitude'] = ''
        item['other_fields'] = ""
        item['coming_soon'] = "0"
        hours = response.xpath('.//div[@class="store-hours"]/span[@class="daily-hours"]')
        item['store_hours'] = ''
        for hour in hours:
            item['store_hours'] += hour.xpath('.//span/text()').extract_first() + hour.xpath('.//text()').extract()[1] + "; " 
        item['store_name'] = response.xpath('.//h1[@class="article-title"]/text()').extract_first()
        address = response.xpath('.//div[@class="store-address"]/text()').extract()
        address = [tp.strip().replace('\n', '') for tp in address if tp.strip() != ""]
        item['address'] = address[0]
        item['address2'] = ''
        item['city'] = address[-2].split(',')[0]
        item['state'] = address[-2].split(',')[1]
        item['zip_code'] = address[-1]
        item['phone_number'] = response.xpath('.//div[@class="store-phone"]/a/text()').extract_first()
        yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

