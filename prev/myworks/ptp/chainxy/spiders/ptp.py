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

class Ptp(scrapy.Spider):
    name = "ptp"

    domain = "http://www.ptpshops.com/"
    start_urls = ["http://www.ptpshops.com/PTP-Truckstop-Network-ALL-Locations.php"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//div[contains(@style, "float: left; padding-left: 30px;")]/p/a[1]/@href').extract()
        for url in url_list:
            request = scrapy.Request(url='http://www.ptpshops.com/%s'
                       % url, callback=self.parse_store)
            request.meta['store_number'] = url.split('?r=')[1].strip()
            yield request

    def parse_store(self, response):
        store_path = response.xpath('.//div[contains(@style, "float: left; padding-left: 30px;")]/p')
        store = store_path.xpath('.//text()').extract()
        try:    
            item = ChainItem()

            if response.meta['store_number'] in self.store_id:
                pass
            item['store_number'] = response.meta['store_number']
            self.store_id.append(response.meta['store_number'])
            item['store_name'] = self.validate(store[0])
            phone = -1
            lat = -1
            hour = -1
            loc = -1
            for x, info in enumerate(store):
                if info.find('Phone') != -1:
                    phone = x
                if info.find('Latitude') != -1:
                    lat = x
                if info.find('Hours of Operation') != -1:
                    hour = x
                if info.find('Location') != -1:
                    loc = x

            item['address2'] =  ''
            item['country'] = 'United States'
            if loc == -1:
                citystatezip = self.parse_citystatezip(self.validate(store[phone-1]))
                item['address'] = self.validate(store[phone-2])
            else:
                citystatezip = self.parse_citystatezip(self.validate(store[loc-1]))
                item['address'] = self.validate(store[loc-2])
            item['city'] = self.validate(citystatezip[0])
            item['state'] = self.validate(citystatezip[1])
            item['zip_code'] = self.validate(citystatezip[2])
            item['phone_number'] = self.validate(store[phone+1])
            item['store_hours'] = self.validate(store[hour+1])
            item['coming_soon'] = "0"
            item['store_hours'] = ''
            item['latitude'] = self.validate(store[lat+1])
            item['longitude'] = self.validate(store[lat+3])
            item['other_fields'] = ''   
            yield item
        except:
            pdb.set_trace()
            
    def validate(self, value):
        if value == None:
            return ""
        else:
            return value.strip()

    def parse_citystatezip(self, value):
        city = self.validate(value.split(',')[0])
        state = self.validate(value.split(',')[1].strip().encode('utf8').replace('\xc2\xa0', '').split(' ')[0])
        zip_code = self.validate(value.split(',')[1].strip().encode('utf8').replace('\xc2\xa0', '').split(' ')[-1])
        return (city, state, zip_code)




        

