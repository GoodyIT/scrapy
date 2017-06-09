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
from lxml import html
import usaddress

class Heidisbrooklyndelibrooklyndeli(scrapy.Spider):
    name = "heidisbrooklyndelibrooklyndeli"

    domain = "www.heidisbrooklyndeli.com"
    start_urls = ["http://heidisbrooklyndeli.com/locations/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//div[@class="list-item-location"]')
        for url in url_list:
            _url = self.validate(url.xpath('.//a[@class="bg-yellow"]/@href').extract_first())
            if _url.strip() == '':
                continue
            address = url.xpath('.//span[1]/text()').extract_first()
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
            request = scrapy.Request(url=_url, callback=self.parse_store)
            request.meta['address'] = address
            request.meta['city'] = city
            request.meta['state'] =  state
            request.meta['zip_code'] =  zip_code
            request.meta['phone_number'] = url.xpath('.//span[2]/text()').extract_first()
            yield request

    def parse_store(self, response):
        item = ChainItem()
        store = response.xpath('.//div[@id="MapDescription"]')
        item['store_number'] = self.validate(response.xpath('.//div[@class="FullMapPage prettyMapList"]//h2[1]/@id').extract_first()).replace('Maplocation-', '')
        item['store_name'] = self.validate(response.xpath('.//div[@class="FullMapPage prettyMapList"]//h2[1]//text()').extract_first())
        address = store.xpath('.//div[@class="address-left"]/text()').extract()
        address = [tp.strip().replace('\n', '') for tp in address if tp.strip() != ""]
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
        item['address'] = address.replace(';', '')
        item['country'] = 'United States'
        item['city'] = city
        item['state'] =  state
        item['zip_code'] =  zip_code
        item['phone_number'] = store.xpath('.//p[1]/text()').extract_first().replace('Phone:', '').strip()
        if item['phone_number'].find('Now Open!') != -1:
            item['phone_number'] = ''
            item['address'] = response.meta['address']
            item['city'] = response.meta['city']
            item['state'] =  response.meta['state']
            item['zip_code'] =  response.meta['zip_code']
        item['latitude'] = ''
        item['longitude'] = ''
        hours = response.xpath('//div[@class="sidebar  push-down-30"]//div[@class="inner-bg"]//dl')
        item['store_hours'] = ''
        for hour in hours:
            item['store_hours'] += " ".join(hour.xpath('.//text()').extract()) + "; "
        item['other_fields'] = ""
        item['coming_soon'] = "0"
        yield item

    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2013', '-').replace(u'\u2019', "'").replace('&#039;', '')
        else:
            return ""





        

