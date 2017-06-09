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

class Theramandbrewery(scrapy.Spider):
    name = "theramandbrewery"

    domain = "http://www.theram.com/"
    start_urls = ["http://www.theram.com/ram-locations/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//div[@id="location-dropdown"]/ul/li/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url= url, callback=self.parse_store)
    
    def parse_store(self, response):
        try:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['store_name'] = self.validate(response.xpath('.//div[@id="tile1"]/h1/text()').extract_first())
            # if item['store_name'].find('WA - Federal Way') != -1:
            #     pdb.set_trace()
            phone = response.xpath('.//div[@id="tile1"]//p[2]/text()').extract()
            phone = [tp.strip().replace('\n', '') for tp in phone if tp.replace('\n', '').strip() != ""]
            address = self.validate(phone[0])
            item['phone_number'] = self.validate(phone[1])
            if len(phone) == 4 or len(phone) == 3 and self.validate(phone[2][-1]).isdigit() and self.validate(phone[1][0]).isdigit() == False:
                item['phone_number'] = self.validate(phone[2])
                address = phone[0] + ' ' + phone[1]
            elif len(phone) == 2 and self.validate(phone[1]).find('.') == -1 and self.validate(phone[1]).find('-') == -1:
                address = phone[0] + ' ' + phone[1]
                item['phone_number'] = ''
            addr = usaddress.parse(address)
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
            item['city'] = city
            item['state'] =  state
            item['zip_code'] =  zip_code
            if item['store_name'].find('OH - Dublin') != -1:
                item['city'] = "Dublin"
                item['state'] =  "Ohio"
                item['zip_code'] =  "43017"
            item['country'] = 'United States'
            
            # if item['store_name'].find('OR - Medford') != -1:
            #     pdb.set_trace()
            item['store_hours'] = "; ".join(response.xpath('.//div[@id="tile1"]/p[1]//text()').extract())
            item['store_hours'] = self.validate(item['store_hours'].lower().replace('we are now open!;', '').strip())
            if item['store_hours'].find('coming ') != -1:
                item['store_hours'] = ''
                item['coming_soon'] = "1"
            yield item
        except:
            pdb.set_trace()
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-').replace(u'\u2013', '-').replace('|', '').replace('\n', '')
        else:
            return ""

    def hasNumbers(self, inputString):
        return not any(char.isdigit() for char in inputString)

    def hasLetters(self, inputString):
        return any(c.isalpha() for c in inputString)





        

