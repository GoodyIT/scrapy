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

class Charlotterusse(scrapy.Spider):
    name = "charlotterusse"

    domain = "http://www.charlotterusse.com"
    start_urls = ["http://www.charlotterusse.com/on/demandware.store/Sites-charlotte-russe-Site/default/Stores-FindByGeoLocation?GeoLocation=(3.1136631,%20101.59998159999998)&Radius=999999&ZipCode=47301&Plus=false&Outlet=false"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//ol[@class="store-listing"]/li/div[@class="store-details"]/a[1]/@href').extract()
        for url in url_list:
            yield scrapy.Request(url="http://www.charlotterusse.com" + url, callback=self.parse_store)
        
    def parse_store(self, response):
        item = ChainItem()
        item['store_number'] = response.url.split('StoreID=')[1]
        item['country'] = 'United States'
        item['latitude'] = ''
        item['longitude'] = ''
        item['store_name'] = self.validate(response.xpath('.//div[@class="store-details-left col-1"]/p[1]/strong/text()').extract_first())
        item['other_fields'] = ""
        item['coming_soon'] = "0"
        _address = response.xpath('.//div[@class="store-details-left col-1"]/p[1]/text()').extract()
        _address = [tp.strip().replace('\n', '') for tp in _address if tp.strip() != ""]
        addr = usaddress.parse(" ".join(_address))
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
        item['phone_number'] =  self.validate(response.xpath('.//div[@class="store-details-left col-1"]/p[1]/a/text()').extract_first())
        hours = response.xpath('.//div[@class="store-details-left col-1"]/p[2]/text()').extract()
        hours = [tp.strip().replace('\n', '') for tp in hours if tp.strip() != ""]
        item['store_hours'] = self.validate('; '.join(hours))
        yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

