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

class Annastaqueria(scrapy.Spider):
    name = "annastaqueria"

    domain = "https://annastaqueria.com/"
    start_urls = ["https://annastaqueria.com/locations"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//div[@class="location_item"]')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            hours = store.xpath('.//div[@class="location-hours"]/p[1]/text()').extract()
            hours = [tp.strip() for tp in hours if tp.strip() != ""]
            if len(hours) == 1:
                item['store_hours'] = "Mon-Sun: " + hours[0]
            else:
                item['store_hours'] =  "; ".join(hours)
            if item['store_hours'].find('Coming Soon') != -1:
                item['store_hours'] = ''
                item['coming_soon'] = "1"
            item['store_name'] = self.validate(store.xpath('.//div[@class="location_title"]/text()').extract_first())
            address = store.xpath('.//div[@class="location-address"]/text()').extract()
            address = [tp.strip() for tp in address if tp.strip() != ""]
            item['address2'] = ''
            addr = usaddress.parse(" ".join(address))
            city = state = zip_code = address = ''
            for temp in addr:
                if temp[1] == 'PlaceName':
                    city += temp[0].replace(',','') + ' '
                elif temp[1] == 'StateName':
                    state = temp[0].replace(',','')
                elif temp[1] == 'ZipCode':
                    zip_code = temp[0].replace(',','')
                else:
                    address += temp[0].replace(',','') + ' '
            item['address'] = address
            item['country'] = 'United States'
            item['city'] = city
            item['state'] =  state
            item['zip_code'] =  zip_code
            item['phone_number'] =  store.xpath('.//div[@class="location-phone"]/text()').extract_first().strip()
            yield item
    
    def validate(self, value):
        if value != None:
            return value.replace('\n', '').replace(u'\u2019', '-').replace('(coming soon)', '').strip()
        else:
            return ""





        

