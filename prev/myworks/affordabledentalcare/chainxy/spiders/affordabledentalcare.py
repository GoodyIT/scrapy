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

import time
from selenium import webdriver
import pdb
import usaddress
from lxml import html

class Affordabledentalcare(scrapy.Spider):
    name = "affordabledentalcare"

    domain = "http://www.affordabledentalcare.com/"
    # start_urls = ["http://www.affordabledentalcare.com/locations/"]
    store_id = []

    def __init__(self):
        self.driver = webdriver.Chrome("./chromedriver")

    def start_requests(self):
        yield scrapy.Request(url=self.domain, callback=self.parse_body)

    def parse_body(self, response):
        self.driver.get("http://www.affordabledentalcare.com/locations/")
        time.sleep(2)
        source = self.driver.page_source.encode("utf8")
        self.driver.close()
        tree = html.fromstring(source)
        url_list = tree.xpath('.//h5[@class="weight-700 uppercase child"]/a/@href')
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse_store)

    def parse_store(self, response):
        item = ChainItem()
        store = response.xpath('.//span[@style="font-size: 18px; line-height: 2;"]/text()').extract()
        store = [tp.strip().replace('\n', '') for tp in store if tp.strip() != ""]
        item['store_number'] = ''
        item['coming_soon'] = "0"
        item['latitude'] = ''
        item['longitude'] = ''
        item['other_fields'] = ""
        item['country'] = 'United States'
        item['store_name'] = response.xpath('.//h2[@class="weight-700 kill-top-margin"]')[0].xpath('.//text()').extract_first().strip()
        
        if len(store) == 0:
            store = response.xpath('.//div[@class="col-md-6"]')[1].xpath('.//p[1]/text()').extract()
        if len(store[0]) > 40:
            store = store[1:]

        idx = 2
        for x,obj in enumerate(store):
            if obj.find('-') != -1:
                idx = x
        address = ''
        if store[0][0].isdigit() == False:
            address = ' '.join(store[1:idx])
        else:
            address = ' '.join(store[:idx])
        item['phone_number'] = store[idx].strip()
        addr = usaddress.parse(address)
        city = state = zip_code = street = ''
        for temp in addr:
            if temp[1] == 'PlaceName':
                city += temp[0].replace(',','') + ' '
            elif temp[1] == 'StateName':
                state = temp[0].replace(',','')
            elif temp[1] == 'ZipCode':
                zip_code = temp[0].replace(',','')
            else:
                street += temp[0].replace(',','') + ' '
        # pdb.set_trace()
        item['address'] = street
        item['city'] = city
        item['state'] =  state
        item['zip_code'] =  zip_code
        if len(store[idx+1:]) != 0:
            item['store_hours'] = self.validate("; ".join(store[idx+1:]))
        else:
            hours = response.xpath('.//div[@class="col-md-6"]')[1].xpath('.//p[3]/text()').extract()
            hours = [tp.strip().replace('\n', '') for tp in hours if tp.strip() != ""]
            item['store_hours'] = self.validate("; ".join(hours))
        # if item['store_name'].find('Arlington/Smokey Point') != -1:
        #     pdb.set_trace()
        yield item
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2013', '-').replace(u'\u2019', "'").replace('&#039;', '')
        else:
            return ""





        

