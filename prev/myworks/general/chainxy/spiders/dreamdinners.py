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

class Dreamdinners(scrapy.Spider):
    name = "dreamdinners"

    domain = "https://dreamdinners.com"
    start_urls = ["https://dreamdinners.com/main.php?page=locations"]
    store_id = []

    def parse(self, response):
        state_list = response.xpath('.//select[@id="zipsearch_state_id"]/option/@value').extract()
        for state in state_list[1:]:
            yield FormRequest(url="https://dreamdinners.com/main.php?page=locations_results", formdata={"state":state}, callback=self.parse_store)

    def parse_store(self, response):
        store_list = response.xpath('.//div[@class="map-content"]/div[contains(@class, "store")]/div[@class="details"]')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_name'] = store.xpath('.//h4/a/text()').extract_first()
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            address = store.xpath('.//div[@class="address"]/div/a/text()').extract()
            address = [tp.strip().replace('\n', '') for tp in address if tp.strip() != ""]
            addr = usaddress.parse(" ".join(address[:-1]))
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
            item['address'] = street
            item['city'] = city
            item['state'] =  state
            item['zip_code'] =  zip_code
            item['address2'] = ''
            item['phone_number'] = address[-1].strip()

            item['store_hours'] = ''
            # pdb.set_trace()
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

