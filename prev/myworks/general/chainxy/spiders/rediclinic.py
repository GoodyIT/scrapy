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

class Rediclinic(scrapy.Spider):
    name = "rediclinic"

    domain = "http://www.rediclinic.com/"
    start_urls = ["http://www.rediclinic.com/clinics/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//ul[@class="state-list"]/li/a/@href').extract()
        for url in url_list:
           yield scrapy.Request(url="https://www.rediclinic.com%s" % url, callback=self.parse_second)

    def parse_second(self, response):
        url_list = response.xpath('.//ul[@class="col-lg-6"]/li[@class="state"]/a/@href').extract()
        for url in url_list:
           yield scrapy.Request(url="https://www.rediclinic.com/clinics%s" % url.replace('..', ''), callback=self.parse_third)

    def parse_third(self, response):
        store_list = response.xpath('.//div[@class="result-entry "]')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = response.xpath('.//div[contains(@class, "clinic-hours")]/div[2]/@id').extract_first().split('-')[-1].strip()
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_name'] = store.xpath('.//div[@class="title"]/a/span/text()').extract_first().strip()
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            address = store.xpath('.//div[@class=" address col-lg-7 col-md-12 col-sm-12 col-xs-12 "]/span/text()').extract()
            addr = usaddress.parse(" ".join(address[:2]))
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
            item['phone_number'] = self.validate(store.xpath('.//div[@class=" address col-lg-7 col-md-12 col-sm-12 col-xs-12 "]/span[3]//text()').extract_first())
            hours = response.xpath('.//div[contains(@class, "clinic-hours")]/div[2]//tr')
            item['store_hours'] = ''
            for hour in hours:
                try:
                    item['store_hours'] += hour.xpath('.//td[1]/text()').extract_first().strip() + ' ' + hour.xpath('.//td[2]/text()').extract_first().strip() + "; "
                except:
                    pass
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

