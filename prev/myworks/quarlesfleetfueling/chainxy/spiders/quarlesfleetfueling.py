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

class Quarlesfleetfueling(scrapy.Spider):
    name = "quarlesfleetfueling"

    domain = "https://quarlesfleetfueling.com/"
    start_urls = ["https://quarlesfleetfueling.com/locations/"]
    store_id = []

    def start_requests(self):
        yield FormRequest(url=self.start_urls[0], formdata={"zip":"27501", "miles_zip":"2000", "submit":"go", "miles":"20"}, headers={'Content-Type':'application/x-www-form-urlencoded'})

    # calculate number of pages
    def parse(self, response):
        store_list = response.xpath('.//ol[@class="listinformation"]/li/div[@class="colm1"]')
        for store in store_list:
            item = ChainItem()
            item['store_number'] =  ''
            item['store_name'] = self.validate(store.xpath('.//h5/text()').extract_first().replace('Site Name:', ''))
            address = self.validate(store.xpath('.//p/text()').extract_first())
            item['city'] = self.validate(address.split(',')[1])
            item['state'] = self.validate(address.split(',')[2].strip().split(' ')[0])
            item['zip_code'] = self.validate(address.split(',')[2].strip().split(' ')[-1])
            item['address'] = self.validate(address.split(',')[0])
            item['address2'] =  ''
            item['country'] = "United States"
            item['phone_number'] = ''
            loc = self.validate(store.xpath('.//a/@href').extract_first().split('?daddr=')[1])
            item['latitude'] =  self.validate(loc.split(',')[0])
            item['longitude'] = self.validate(loc.split(',')[1])
            item['store_hours'] = ''
            item['other_fields'] = ""
            item['coming_soon'] = "0"    

            yield item

    def validate(self, value):
        if value == None:
            return ""
        else:
            return value.strip().replace(u'\u2013', '-')








        

