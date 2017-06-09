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

class Deandeluca(scrapy.Spider):
    name = "deandeluca"

    domain = "http://www.deandeluca.com/"
    start_urls = ["http://www.deandeluca.com/store-locations"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//section[@class="section"]')
        for url in url_list:
            if url.xpath('.//h2/text()').extract_first().find('International') != -1:
                break;
            second_list = url.xpath('.//div[@class="overlay"]/a[@class="link"]/@href').extract()
            for second in second_list:
                yield scrapy.Request(url=second, callback=self.parse_store)
        
    def parse_store(self, response):
        try:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_name'] = self.validate(' '.join(response.xpath('.//div[@class="title"]/h1/text()').extract()))
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            address = response.xpath('.//address/a/text()').extract()
            address = [tp.strip() for tp in address if tp.strip() != ""]
            addr = usaddress.parse(" ".join(address))
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
            item['address2'] = ''
            item['phone_number'] = self.validate(response.xpath('.//ul[@class="location-info"]/li[3]/p/text()').extract_first().split(':')[1])
            hours = response.xpath('.//ul[@class="location-info"]/li[2]/p/text()').extract()
            hours = [tp.strip() for tp in hours if tp.strip() != ""]
            item['store_hours'] = '; '.join(hours)

            yield item
        except:
            pdb.set_trace()
        
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-').replace(u'\u2013', '-')
        else:
            return ""





        

