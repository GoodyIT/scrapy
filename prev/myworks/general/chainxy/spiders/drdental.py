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

class Drdental(scrapy.Spider):
    name = "drdental"

    domain = "https://www.mydrdental.com/"
    start_urls = ["https://www.mydrdental.com/locations/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//div[@class="addresses"]//div[@class="address"]//a/@href').extract()
        for url in url_list:
            if url.strip() != '':
                yield scrapy.Request(url=url, callback=self.parse_store)
        
    def parse_store(self, response):
        try:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_name'] = self.validate(response.xpath('.//div[@id="main_header"]/h1/text()').extract_first())
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            _address = response.xpath('.//div[@itemprop="address"]/text()').extract_first().strip()
            addr = usaddress.parse(_address)
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
            item['address'] = street
            item['address2'] = ''
            item['phone_number'] = response.xpath('.//span[@class="mm-phone-number"]/text()').extract_first()
            hours = response.xpath('.//ul[@class="loc_hours"]/li')
            item['store_hours'] = ''
            for hour in hours:
                item['store_hours'] +=  hour.xpath('.//text()').extract_first() + hour.xpath('.//text()').extract()[1] + "; " 

            yield item
        except:
            pdb.set_trace()
        
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-').replace(u'\u2013', '-')
        else:
            return ""





        

