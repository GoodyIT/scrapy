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

class Mothersmarket(scrapy.Spider):
    name = "mothersmarket"

    domain = "http://www.mothersmarket.com/"
    start_urls = ["http://www.mothersmarket.com/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//select[@name="jumpmenu"]/option/@value').extract()
        for url in url_list:
            if url.strip() != '':
                yield scrapy.Request(url="http://www.mothersmarket.com" + url, callback=self.parse_store)
        
    def parse_store(self, response):
        info = response.xpath('.//div[@class="location-desc grid_3"]/p')
        item = ChainItem()
        item['store_number'] = ''
        item['country'] = 'United States'
        item['latitude'] = ''
        item['longitude'] = ''
        item['store_name'] = self.validate(response.xpath('.//li[@itemprop="itemListElement"]')[1].xpath('.//span/text()').extract_first())
        item['other_fields'] = ""
        item['coming_soon'] = "0"
        _address = info[0].xpath('.//text()').extract()
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
        item['address2'] = ''
        item['phone_number'] = self.validate(info[1].xpath('.//text()').extract_first())
        hours = info[-1].xpath('.//text()').extract()
        hours = [tp.strip().replace('\n', '') for tp in hours if tp.strip() != ""]
        item['store_hours'] = self.validate('; '.join(hours))
        yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-').replace(u'\u2013', '-').split('Juice Bar')[0].split('Cafe and Restaurant')[0]
        else:
            return ""





        

