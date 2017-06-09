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

class Carmart(scrapy.Spider):
    name = "carmart"

    domain = "http://www.car-mart.com/"
    start_urls = ["http://www.car-mart.com/Home/Locations"]
    store_id = []

    def parse(self, response):
        state_list = response.xpath('.//select[@id="SelectedState"]/option/text()').extract()
        for state in state_list:
            yield scrapy.Request(url= "http://www.car-mart.com/Home/GetLotDropDownList?state=" + state, callback=self.parse_city)

    def parse_city(self, response):
        store_list = json.loads(response.body)
        for store in store_list:
            yield scrapy.Request(url= "http://www.car-mart.com/Home/GetLotInformation?lotNumber=" + store['Value'], callback=self.parse_store)
    
    def parse_store(self, response):
        item = ChainItem()
        item['store_number'] = ''
        item['country'] = 'United States'
        item['latitude'] =  ''
        item['longitude'] = ''
        item['other_fields'] = ""
        item['coming_soon'] = "0"
        item['address2'] = ''
        # pdb.set_trace()
        item['store_name'] = self.validate(response.xpath('.//tr[1]//span/text()').extract_first())
        item['store_hours'] = self.validate(response.xpath('.//tr[4]//td[2]/text()').extract_first())
        address = response.xpath('.//tr[2]//td[2]/text()').extract()
        address = [tp.strip().replace('\n', '') for tp in address if tp.strip() != ""]
        addr = usaddress.parse(" ".join(address))
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
        item['phone_number'] = self.validate(response.xpath('.//tr[3]//td[2]/text()').extract_first())
        yield item
    
    def validate(self, value):
        if value != None:
            return value.replace(u'\u2019', '-').replace('Hours:', '').strip()
        else:
            return ""





        

