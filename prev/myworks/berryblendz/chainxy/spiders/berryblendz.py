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

class Berryblendz(scrapy.Spider):
    name = "berryblendz"

    domain = "http://berryblendz.com/"
    start_urls = ["http://berryblendz.com/find-a-store.php"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//p[@style="margin-bottom: 25px;"]/a/@href').extract()
        for url in url_list[1:]:
            yield scrapy.Request(url="http://berryblendz.com" + url, callback=self.parse_store)
                
    def parse_store(self, response):
        store_list = response.xpath('.//p[@style="margin-bottom: 10px;"]')
        for store in store_list:
            info = store.xpath('.//text()').extract()
            item = ChainItem()
            try:
                item['store_number'] = ''
                address = [tp.strip() for tp in info if tp.strip() != ""]
                

                if info[0].find('Coming soon') != -1:
                    item['coming_soon'] = "1"
                    item['store_name'] = 'Castle Rock'
                    yield item
                else:
                    loc = -1
                    for x, value in reversed(list(enumerate(info))):
                        if value.find(',') != -1:
                            loc = x
                            break

                    item['address'] = self.validate(' '.join(info[0:loc-1]))
                    if item['address'].strip() == '':
                        item['address'] = self.validate(' '.join(info[0:loc]))
                    item['address2'] = ''
                    item['country'] = 'United States'
                    item['city'] = self.validate(info[loc].split(',')[0])
                    item['store_name'] = item['city'] 
                    item['state'] = self.validate(info[loc].split(',')[1].strip().split(' ')[0])
                    item['zip_code'] = self.validate(info[loc].split(',')[1].strip().split(' ')[1])
                    try:
                        item['phone_number'] = self.validate(info[loc+1].replace('Ph:', ''))
                    except:
                        item['phone_number'] = ''
                    # if item['store_name'].find('17659 Glasgow Avenue') != -1:
                    #     pdb.set_trace()
                    item['latitude'] = ''
                    item['longitude'] = ''
                    item['store_hours'] = ''
                    item['other_fields'] = ""
                    item['coming_soon'] = "0"
                    yield item
            except:
                pdb.set_trace()
                

    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2013', '-').replace(u'\u2019', "'")
        else:
            return ""





        

