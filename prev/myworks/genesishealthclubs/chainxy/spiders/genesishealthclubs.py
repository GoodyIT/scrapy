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

class Genesishealthclubs(scrapy.Spider):
    name = "genesishealthclubs"

    domain = "http://www.genesishealthclubs.com/"
    start_urls = ["http://www.genesishealthclubs.com/locations"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        url_list = response.xpath('.//span[@class="location-title"]/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url='http://www.genesishealthclubs.com%s' % url, callback=self.parse_store)
            
    def parse_store(self, response):
        item = ChainItem()

        item['store_number'] = ''
        item['store_name'] = self.validate(response.xpath('.//div[@class="location-name"]/text()').extract_first())
        addr = usaddress.parse(self.validate(response.xpath('.//div[@class="location-address"]/text()').extract_first()))
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
        item['latitude'] = ''
        item['longitude'] = ''
        item['country'] = 'United States'
        item['phone_number'] = self.validate(response.xpath('.//div[@class="location-phone"]/text()').extract_first())
        hours = response.xpath('.//div[@id="location-hours-tip"]/div')
        item['store_hours'] = ''
        for hour in hours:
            item['store_hours'] += "".join(hour.xpath('.//text()').extract()) + "; "
        
        item['other_fields'] = ""
        item['coming_soon'] = "0"

        yield item

    def validate(self, value):
        if value != None:
            return value.strip()
        else:
            return ""





        

