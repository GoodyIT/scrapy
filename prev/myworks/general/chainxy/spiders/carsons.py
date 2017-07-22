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

class Carsons(scrapy.Spider):
    name = "carsons"

    domain = "https://www.carsons.com"
    start_urls = ["https://stores.carsons.com/"]
    store_id = []

    state = dict()

    def parse(self, response):
        state_list = response.xpath('.//div[@class="tlsmap_list"]//a/@href').extract()
        for state in state_list:
            yield scrapy.Request(url=state, callback=self.parse_second)

    def parse_second(self, response):
        state_list = response.xpath('.//div[@class="tlsmap_list"]//a/@href').extract()
        for state in state_list:
            yield scrapy.Request(url=state, callback=self.parse_store)

    def parse_store(self, response):
        store_list = response.xpath('.//div[@class="tlsmap_list"]//div[@class="map-list-item"]')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store.xpath('.//div[@class="json-hours"]/@data-lid').extract_first()
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_name'] = store.xpath('.//a[contains(@class, "location-name")]/text()').extract_first()
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store.xpath('.//div[@class="addr"]')[1].xpath('.//text()').extract_first()
            try:
                item['address2'] = store.xpath('.//div[@class="addr"]')[1].xpath('.//text()').extract_first()
            except:
                item['address2'] = ''
            parse_citystatezip = self.parse_citystatezip(store.xpath('.//div[@class="csz"]/text()').extract_first().strip())
            item['city'] = parse_citystatezip[0]
            item['state'] = parse_citystatezip[1]
            item['zip_code'] = parse_citystatezip[2]
            item['phone_number'] =  store.xpath('.//div[@class="phone"]/a/text()').extract_first()
            hours = store.xpath('.//div[@class="json-hours"]/div[@class="hours"]/div/meta/@content').extract()
            item['store_hours'] = '; '.join(hours)

            if item['state'] not in self.state:
                self.state[item['state']] = 0
            self.state[item['state']] += 1
            yield item
            print self.state
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""

    def parse_citystatezip(self, value):
        city = self.validate(value.split(',')[0])
        state = self.validate(value.split(',')[1].strip().split(' ')[0])
        zip_code = self.validate(value.split(',')[1].strip().split(' ')[-1])
        return (city, state, zip_code)






        

