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

class Kneaders(scrapy.Spider):
    name = "kneaders"

    domain = "http://www.o2fitnessclubs.com/"
    start_urls = ["https://www.kneaders.com/Locations"]
    store_id = []

    def parse(self, response):
        state_list = response.xpath('.//div[contains(@class, "resource_menu_actions")]/a/@href').extract()
        for state in state_list:
            request = scrapy.Request(url="https://www.kneaders.com/%s" % state, callback=self.parse_store)

            request.meta['state'] = state
            yield request

    def parse_store(self, response):
        store_list = response.xpath('.//div[@class="resource_locations_location"]')
        for store in store_list:
            try:
                item = ChainItem()

                item['store_number'] = ''
                item['store_name'] = store.xpath('.//div[@class="resource_locations_location_content_title"]/text()').extract_first().replace(u'\u2013', '')
                address = store.xpath('.//div[@class="resource_locations_location_content_address"]/text()').extract_first()
                if len(address.split(',')) == 3:
                    if len(address.split(',')[2].strip().split(' ')) == 1:
                        item['address'] = address.split(',')[0].strip().split('|')[0].strip()
                        item['city'] = address.split(',')[0].strip().split('|')[1].strip()
                        item['state'] = address.split(',')[1].strip()
                        item['zip_code'] = address.split(',')[2].strip()
                    else:
                        item['address'] = address.split(',')[0].strip()
                        item['city'] = address.split(',')[1].strip()
                        item['state'] = address.split(',')[2].strip().split(' ')[0].strip()
                        item['zip_code'] = address.split(',')[2].strip().split(' ')[1].strip()
                else:
                    item['address'] = address.split(',')[0].strip().split('|')[0].strip()
                    item['city'] = address.split(',')[0].strip().split('|')[1].strip()
                    item['state'] = address.split(',')[1].strip().split(' ')[0].strip()
                    item['zip_code'] = address.split(',')[1].strip().split(' ')[1].strip()
                
                # if item['store_name'].find('ARAPAHOE') != -1:
                #     pdb.set_trace()
                item['address2'] = ''
                item['country'] = 'United States'

                item['phone_number'] = store.xpath('.//div[@class="resource_locations_location_content_phone"]/text()').extract_first().replace('Ph', '').strip().split('|')[0]
                item['latitude'] = ''
                item['longitude'] = ''

                item['store_hours'] = store.xpath('.//div[@class="resource_locations_location_content_hours"]/text()').extract_first()
                item['other_fields'] = ""
                item['coming_soon'] = "0"
            except:
                pdb.set_trace()
            yield item




        

