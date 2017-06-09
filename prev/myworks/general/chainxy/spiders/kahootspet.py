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

class Kahootspet(scrapy.Spider):
    name = "kahootspet"

    domain = "http://kahootsfeedandpet.com/"
    start_urls = ["http://kahootsfeedandpet.com/locations/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//div[contains(@class, "group post")]/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url= url, callback=self.parse_store)

    def parse_store(self, response):
        item = ChainItem()
        item['store_number'] = response.xpath('.//div[contains(@class, "portfolio type-portfolio")]/@id').extract_first().split('-')[1]
        item['country'] = 'United States'
        item['latitude'] = ''
        item['longitude'] = ''
        item['store_name'] = response.xpath('.//div[@class="col-location-1"]//h2[1]/text()').extract_first()
        item['other_fields'] = ""
        address = response.xpath('.//div[@class="col-location-2"]/p[2]/text()').extract()
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
        item['phone_number'] =  address[-1].replace('Phone', '').strip()
        hours = response.xpath('.//div[@class="col-location-2"]/p[3]/text()').extract()
        hours = [tp.strip().replace('\n', '') for tp in hours if tp.strip() != ""]
        item['store_hours'] = "; ".join(hours)
        
  
        yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

