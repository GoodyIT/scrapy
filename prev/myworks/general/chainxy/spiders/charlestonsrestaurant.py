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

class Charlestonsrestaurant(scrapy.Spider):
    name = "charlestonsrestaurant"

    domain = "http://ehsrg.com/"
    start_urls = ["http://ehsrg.com/restaurants/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//div[@class="big-text center-it"]/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse_second)

    def parse_second(self, response):
        url_list = response.xpath('.//div[@class="location clearfix"]/a[@class="button left"]/@href').extract()
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse_store)

    def parse_store(self, response):
        try:
            item = ChainItem()
            item['store_number'] = ''
            
            item['store_name'] = self.validate(response.xpath('.//div[@class="main left"]/h1/text()').extract_first())
            try:
                address = response.xpath('.//div[@class="half left"]//a/text()')[0].extract() + ' ' + response.xpath('.//div[@class="half left"]//a/text()')[1].extract()
            except:
                address = response.xpath('.//div[@class="main left"]/div[1]//text()').extract() 
                address = [tp.strip() for tp in address if tp.strip() != ""]
                address = address[0]

            loc = ''
          
            item['phone_number'] = response.xpath('.//p[@class="numbers"]/text()').extract_first().strip().replace('Phone:', '').strip()
            hours = response.xpath('.//div[@class="hours clearfix"]')
            item['store_hours'] = ''
            try:
                for hour in hours:
                    item['store_hours'] +=  hour.xpath('.//p[@class="left"]/text()').extract_first() + ' ' + hour.xpath('.//p[@class="right"]/text()').extract_first() + "; "
            except:
                item['store_hours'] = ''
            item['coming_soon'] = "0"
            item['latitude'] = ''
            item['longitude'] = ''
            item['other_fields'] = ""
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
            item['country'] = 'United States'
            item['city'] = city
            item['state'] =  state
            item['zip_code'] =  zip_code
            yield item
        except:
            pdb.set_trace()
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2013', '-').replace(u'\u2019', "'").replace('&#039;', '')
        else:
            return ""





        

