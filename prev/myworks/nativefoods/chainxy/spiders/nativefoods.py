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

class Nativefoods(scrapy.Spider):
    name = "nativefoods"

    domain = "http://www.nativefoods.com/"
    start_urls = ["http://www.nativefoods.com/"]
    store_id = []

    def parse(self, response):
        state_list = response.xpath('.//div[contains(@class, "item prevent active")]/div/a/@href').extract()
        for state in state_list:
            request = scrapy.Request(url="https://www.nativefoods.com%s" % state, callback=self.parse_store)
            yield request

    def parse_store(self, response):
        if response.url.find('springs') != -1:
            item = ChainItem()

            item['store_name'] = response.xpath('.//div[@class="address"]/p[1]/text()').extract_first().strip()
            item['address'] = response.xpath('.//div[@class="address"]/p[2]/text()').extract_first().strip()
            item['city'] = response.xpath('.//div[@class="address"]/p[3]/text()').extract_first().split(',')[0].strip()
            item['state'] = response.xpath('.//div[@class="address"]/p[3]/text()').extract_first().split(',')[1].strip().split(' ')[0].strip()
            item['zip_code'] = response.xpath('.//div[@class="address"]/p[3]/text()').extract_first().split(',')[1].strip().split(' ')[1].strip()
            item['phone_number'] = response.xpath('.//div[@class="contact"]/p/a/text()').extract_first()
            item['store_hours'] = response.xpath('.//div[@class="hours"]/div/span[1]/text()').extract_first().strip() + ' ' + response.xpath('.//div[@class="hours"]/div/span[2]/text()').extract_first().strip().replace(u'\u2013', '-')
            item['store_number'] = ''
            item['address2'] = ''
            item['country'] = 'United States'

            item['latitude'] = ''
            item['longitude'] = ''

            item['other_fields'] = ""
            item['coming_soon'] = "0"
            yield item
        else:    
            store_list = response.xpath('.//div[@class="map-details"]')
            for store in store_list:
                item = ChainItem()
                    
                item['store_name'] = store.xpath('.//div[@class="title"]/text()').extract_first().replace(u'\u2013', '')
                item['address'] = store.xpath('.//div[@class="address"]/p[@class="line1"]/text()').extract_first()
                item['city'] = store.xpath('.//div[@class="address"]/p[@class="line2"]/text()').extract_first().split(',')[0]
                item['state'] = store.xpath('.//div[@class="address"]/p[@class="line2"]/text()').extract_first().split(',')[1].strip().split(' ')[0]
                item['zip_code'] = store.xpath('.//div[@class="address"]/p[@class="line2"]/text()').extract_first().split(',')[1].strip().split(' ')[1]
                item['phone_number'] = store.xpath('.//div[@class="address"]/p[@class="phone"]/a/text()').extract_first()
                item['store_hours'] = store.xpath('.//div[@class="address"]/p[contains(@class, "hours")]/text()').extract_first().replace('Hours:', '').strip().replace(u'\u2013', '-')
                    
                item['store_number'] = ''
                item['address2'] = ''
                item['country'] = 'United States'

                item['latitude'] = ''
                item['longitude'] = ''

                item['other_fields'] = ""
                item['coming_soon'] = "0"
                
                yield item




        

