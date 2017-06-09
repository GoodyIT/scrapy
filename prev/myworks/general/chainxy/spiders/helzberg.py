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

class Helzberg(scrapy.Spider):
    name = "helzberg"

    domain = "https://www.helzberg.com/"
    start_urls = ["https://www.helzberg.com/store-locator/all-stores.do"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//div[contains(@class, "eslStore ml-storelocator-headertext")]/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url= "https://www.helzberg.com" + url, callback=self.parse_store)

    def parse_store(self, response):
        item = ChainItem()
        item['store_number'] = ''
        item['country'] = 'United States'
        item['latitude'] = ''
        item['longitude'] = ''
        item['store_name'] = response.xpath('.//div[@class="ml-storelocator-store-address"]//div[@class="eslStore"]/text()').extract_first()
        item['other_fields'] = ""
        item['address'] = response.xpath('.//div[@class="ml-storelocator-store-address"]//div[@class="eslAddress1"]/text()').extract_first().strip()
        item['city'] = response.xpath('.//div[@class="ml-storelocator-store-address"]//span[@class="eslCity"]/text()').extract_first().replace(',', '').strip()
        item['state'] =  response.xpath('.//div[@class="ml-storelocator-store-address"]//span[@class="eslStateCode"]/text()').extract_first().strip()
        item['zip_code'] =  response.xpath('.//div[@class="ml-storelocator-store-address"]//span[@class="eslPostalCode"]/text()').extract_first().strip()
        item['phone_number'] =  response.xpath('.//div[@class="ml-storelocator-store-address"]//div[@class="eslPhone"]/text()').extract_first().strip()
        hours = response.xpath('.//span[@class="ml-storelocator-hours-details"]/text()').extract()
        hours = [tp.strip().replace('\n', '') for tp in hours if tp.strip() != ""]
        item['store_hours'] = "; ".join(hours)
        item['coming_soon'] = "0"
  
        yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

