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

class Comchop(scrapy.Spider):
    name = "comchop"

    domain = "http://bobs-steakandchop.com/"
    start_urls = ["http://bobs-steakandchop.com/amelia-island/locations/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//div[@class="medium-4 columns left"]/div/div/h5/a')
        for store_url in url_list:
            url = ''
            try:
                url = self.validate(store_url.xpath('.//@href').extract_first())
                yield scrapy.Request(url=url, callback=self.parse_store)
            except:
                self.parse_coming_soon(store_url.xpath('.//text()').extract_first())
                
    def parse_coming_soon(self, name):
        pdb.set_trace()
        item = ChainItem()
        item['store_name'] = self.validate(name.split('(')[0])
        yield item
        
    def parse_store(self, response):
        item = ChainItem()
        try:
            item['store_number'] = ''
            item['store_name'] = self.validate(response.xpath('.//h3[@class="fancy-title"]/text()').extract_first())
            address = response.xpath('.//div[@class="ph1 hours-wrap"]/p/text()').extract()
            address = [tp.strip() for tp in address if tp.strip() != ""]

            item['address'] = self.validate(address[0].split(',')[0].strip().split('\r\n')[0])
            item['address2'] = ''
            item['country'] = 'United States'
            # if item['address'].find('80 Amelia Village Circle') != -1:
            #     pdb.set_trace()
            if len(address) == 2:
                item['city'] = self.validate(address[0].split(',')[0].strip().split('\r\n')[1])
                item['state'] = self.validate(address[0].split(',')[1].strip().split('\r\n')[0].split(' ')[0])
                item['zip_code'] = self.validate(address[0].split(',')[1].strip().split('\r\n')[0].split(' ')[1])
                item['phone_number'] = address[1]
            elif len(address) == 3:
                pdb.set_trace()
                try:
                    item['address'] = self.validate(address[0].split('\r\n')[0].strip())
                    item['city'] = self.validate(address[0].split('\r\n')[1].strip())
                    item['state'] = self.validate(address[1].strip().split('\r\n')[0].split(' ')[0])
                    item['zip_code'] = self.validate(address[1].strip().split('\r\n')[0].split(' ')[1])
                    item['phone_number'] = self.validate(address[1].strip().split('\r\n')[1].strip())
                except:
                    item['city'] = self.validate(address[2].split(',')[0].strip())
                    item['state'] = self.validate(address[2].split(',')[1].strip().split('\r\n')[0].split(' ')[0])
                    item['zip_code'] = self.validate(address[2].split(',')[1].strip().split('\r\n')[0].split(' ')[1])
                    item['phone_number'] = self.validate(address[3].split(',')[0].strip())
            elif len(address) == 4:
                item['city'] = self.validate(address[0].split(',')[0].strip().split('\r\n')[1])
                item['state'] = self.validate(address[0].split(',')[1].strip().split('\r\n')[0].split(' ')[0])
                item['zip_code'] = self.validate(address[0].split(',')[1].strip().split('\r\n')[0].split(' ')[1])
                item['phone_number'] = self.validate(address[0].split(',')[1].strip().split('\r\n')[-1])
            elif len(address) == 5:
                item['address2'] = address[1]
                item['city'] = self.validate(address[2].split(',')[0].strip().split('\r\n')[1])
                item['state'] = self.validate(address[2].split(',')[1].strip().split('\r\n')[0].split(' ')[0])
                item['zip_code'] = self.validate(address[2].split(',')[1].strip().split('\r\n')[0].split(' ')[1])
                item['phone_number'] = self.validate(address[2].split(',')[1].strip().split('\r\n')[-1])
            else: 
                item['address2'] = address[1]
                item['city'] = self.validate(address[2].split(',')[0].strip())
                item['state'] = self.validate(address[2].split(',')[1].strip().split('\r\n')[0].split(' ')[0])
                item['zip_code'] = self.validate(address[2].split(',')[1].strip().split('\r\n')[0].split(' ')[1])
                item['phone_number'] = self.validate(address[2].split(',')[1].strip().split('\r\n')[-1])

            item['latitude'] = ''
            item['longitude'] = ''

            item['store_hours'] = ''
            hours = response.xpath('.//div[@class="ph1 hours-wrap"]/div[@class="mb2"]/p')
            for hour in hours:
                item['store_hours'] += self.validate(" ".join(hour.xpath('.//text()').extract())).replace('\n', '').replace('\r', ' ') + "; "

            item['other_fields'] = ""
            item['coming_soon'] = "0"
            yield item
        except:
            pdb.set_trace()
                

    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2013', '-')
        else:
            return ""





        

