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

class Cba(scrapy.Spider):
    name = "cba"

    domain = "http://cbaonline.org/"
    start_urls = ["http://cba.know-where.com/cba/cgi/rollover?region_cue=1&mapid=US&ht=256&wd=406&mapGif=Icon/US.gif&blank=Icon/blank_maps/US.blank.gif"]
    store_name = []
    phone_number = []

    def __init__(self):
        ca_json = open('citiesusca.json', 'rb')
        self.ca_long_lat_fp = json.load(ca_json)

    def parse(self, response):
        for city in self.ca_long_lat_fp:
            if self.ca_long_lat_fp[city]["country"] == "United States":
                request =  scrapy.Request(url="http://cba.know-where.com/cba/cgi/selection?mapx=0&mapy=0&mapid=US&lang=en&design=default&country=&region_name=&region=&place=%s&x=63&y=33" % self.ca_long_lat_fp[city]["zip_code"], callback=self.parse_store)
                yield request

    # def parse_second(self, response):
    #     region_name = response.xpath("//script[contains(., 'kw_region_name =')]/text()").extract_first().split('kw_region_name =')[1].strip().split('kw_mapid =')[0].replace(';', '')
    #     yield scrapy.Request(url="http://cba.know-where.com/cba/cgi/selection?state-map=%s&map.x=196&map.y=124&mapid=US&lang=en&design=default&country=US&region_name=%s&region=&place=" % (request.meta['state'], region_name), callback=self.parse_third)

    def parse_store(self, response):
        try:
            store_list = response.xpath('.//table[@class="kwresults_table"]//tr')
            for store in store_list[1:]:
                item = ChainItem()
                item['phone_number'] = store.xpath('.//td[2]/font//text()').extract_first().strip()
                if item['phone_number'] in self.phone_number:
                    continue
                self.phone_number.append(item['phone_number'])
                
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                info = store.xpath('.//td[1]/font//text()').extract()
                info = [tp.strip().replace('\n', '') for tp in info if tp.replace('\n', '').strip() != ""]
                item['store_name'] = info[0].split('#')[0].strip()
                if len(info[0].split('#')) > 1:
                    item['store_number'] = info[0].split('#')[1].strip()
                else:
                    item['store_number'] = ''

                item['other_fields'] = ""
                item['coming_soon'] = "0"
                addr = usaddress.parse(" ".join(info[1:]))
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
                item['store_hours'] = ''
                yield item
        except:
            pdb.set_trace()
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

