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

class Affordabledentalcare(scrapy.Spider):
    name = "affordabledentalcare"

    domain = "http://www.affordabledentalcare.com/"
    start_urls = ["http://www.affordabledentalcare.com/locations/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//div[@class="location"]/div[@class="title"]/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse_store)

    def parse_store(self, response):
        try:
            item = ChainItem()
            store = response.xpath('.//div[@id="MapDescription"]')
            item['store_number'] = ''
            
            item['store_name'] = self.validate(response.xpath('.//h1[@class="entry-title"]/text()').extract_first())
            address = response.xpath('.//div[@class="col-2"]/div[@class="inner"]/p[1]/text()').extract()
            address = [tp.strip().replace('\n', '') for tp in address if tp.strip() != ""]
            loc = ''
            if len(address) == 0:
                address = response.xpath('.//div[@class="entry-content"]/p[1]/text()').extract()
                address = [tp.strip().replace('\n', '') for tp in address if tp.strip() != ""]
                hours = response.xpath('.//div[@class="entry-content"]/p[2]/text()').extract_first()
                if hours.find('Coming Soon!') != -1:
                    item['coming_soon'] = "1"
                    item['store_hours'] = ''
                loc = response.xpath('.//div[@class="entry-content"]/script[2]/text()').extract_first().strip().split('google.maps.LatLng(')[1].strip().split(');')[0].encode('utf8').replace('\xc2\xb0', '')
            else:
                item['phone_number'] = response.xpath('.//div[@class="col-2"]/div[@class="inner"]/p[3]/text()').extract_first().strip().split('**')[0].split('*')[0]
                hours = response.xpath('.//div[@class="col-2"]/div[@class="inner"]/p[2]/text()').extract()
                hours = [tp.strip().replace('\n', '') for tp in hours if tp.strip() != ""]
                if hours[-1].find('-') == -1:
                    hours = hours[:-1]
                if hours[0].find('-') == -1:
                    hours = hours[1:]
                item['store_hours'] = "; ".join(hours).replace('.', ' ').replace(u'\u2013', '-')
                item['coming_soon'] = "0"
                loc = response.xpath('.//div[@class="col-2"]/div[@class="inner"]/script[2]/text()').extract_first().strip().split('google.maps.LatLng(')[1].strip().split(');')[0].encode('utf8').replace('\xc2\xb0', '')

            item['latitude'] = loc.split(',')[0]
            item['longitude'] = loc.split(',')[1]
            item['other_fields'] = ""
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
            yield item
        except:
            pdb.set_trace()
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2013', '-').replace(u'\u2019', "'").replace('&#039;', '')
        else:
            return ""





        

