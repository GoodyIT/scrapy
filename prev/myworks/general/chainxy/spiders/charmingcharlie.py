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

class Charmingcharlie(scrapy.Spider):
    name = "charmingcharlie"

    domain = "http://www.charmingcharlie.com"
    start_urls = ["http://stores.charmingcharlie.com/search"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath("//script[contains(., 'RLS.defaultData = ')]/text()").extract_first().split('RLS.defaultData = ')[1].strip().replace('\\', '').split(' View all locations in')
        for url in url_list[1:]:
            _url = url.split('href=')[1].split('target="_parent"')[0].strip()[1:-1]

            yield scrapy.Request(url=_url, callback=self.parse_second)
             

    def parse_second(self, response):
        url_list = response.xpath('.//div[@class="tlsmap_list"]/li/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse_third)

    def parse_third(self, response):
        url_list = response.xpath('.//div[@class="city-tlsmap-box-re-skin"]')
        for url in url_list:
            request = scrapy.Request(url=url.xpath('.//div[@class="grid_5 omega"]/div/div[@class="store-info"]/a/@href').extract_first(), callback=self.parse_store)
            request.meta['id'] = url.xpath('.//@data-lid').extract_first()
            yield request

    def parse_store(self, response):
        try:
            item = ChainItem()
            _address = response.xpath('.//p[@class="address"]/span/text()').extract()
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

            if zip_code.strip() == '' or state.find('SA-02') != -1 or city.find('Dubai') != -1:
                return
            elif zip_code.isdigit() == False:
                item['address'] = _address[0]
                item['city'] = _address[-1].split(',')[0]
                item['state'] =  _address[-1].split(',')[1].strip().split(' ')[0]
                item['zip_code'] =  ' '.join(_address[-1].split(',')[1].strip().split(' ')[1:])
                item['country'] = 'Canada'
            else:
                item['address'] = _address[0]
                item['city'] = city
                item['state'] =  state
                item['zip_code'] =  zip_code
                item['country'] = 'United States'

            if len(_address) == 3:
                item['address2'] = _address[1]
                
            item['store_number'] = response.meta['id']
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_name'] = self.validate(response.xpath('.//span[@class="location-name"]/text()').extract_first())
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            
            item['phone_number'] =  self.validate(response.xpath('.//div[@class="inner-content"]/div[@class="right"]/a/text()').extract_first())
            hours = response.xpath('.//div[@class="hoursContainer"]/div[@class="day-hour-row"]/meta/@content').extract()
            hours = [tp.strip().replace('\n', '') for tp in hours if tp.strip() != ""]
            item['store_hours'] = self.validate('; '.join(hours))
            yield item
        except:
            pdb.set_trace()
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-').replace(u'\u2013', '-')
        else:
            return ""





        

