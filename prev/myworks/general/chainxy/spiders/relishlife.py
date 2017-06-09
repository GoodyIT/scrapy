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

class Relishlife(scrapy.Spider):
    name = "relishlife"

    domain = "http://www.relishlife.com/"
    start_urls = ["http://relishlife.com/locations/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//div[@class="image_wrapper"]/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse_store)

    def parse_store(self, response):
        item = ChainItem()
        item['store_number'] = ''
        item['country'] = 'Canada'
        item['latitude'] = ''
        item['longitude'] = ''
        item['store_name'] = self.validate(response.xpath('.//div[@class="get_in_touch"]/h3/text()').extract_first())
        item['other_fields'] = ""
        item['coming_soon'] = "0"
        address = response.xpath('.//span[@class="address_wrapper"]//text()').extract()
        address = [tp.strip() for tp in address if tp.replace('\n', '').strip() != ""]
        item['address'] = address[0]
        item['address2'] = ''
        item['city'] = address[1].split('\n')[0].split(',')[0]
        item['state'] = address[1].split('\n')[0].split(',')[1]
        item['zip_code'] = address[1].split('\n')[1]
        item['phone_number'] = response.xpath('.//li[@class="phone"]/p/a/text()').extract_first()
        item['store_hours'] = ''
        yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-').replace(u'\u2013', '-')
        else:
            return ""





        

