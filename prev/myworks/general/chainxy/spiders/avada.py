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

class avada(scrapy.Spider):
    name = "avada"

    domain = "http://www.avada.com/"
    start_urls = ["http://www.avada.com/locations/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//div[@class="sabai-directory-category-title"]/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url = url, callback=self.parse_store)

    def parse_store(self, response):
        page_count = response.xpath('.//div[@class="sabai-pagination sabai-btn-group"]/a').extract()
        if len(page_count) > 2:
            for x in range(1,len(page_count)-1):
                category = 8
                if response.url.find('wisconsin') != -1:
                    category = 15
                yield scrapy.Request(url=response.url + "/listings?p="+str(x)+"&category="+str(category)+"&zoom=15&is_mile=1&directory_radius=20&view=list&sort=title&__ajax=%23sabai-inline-content-listings%20.sabai-directory-listings-container&_=1496851950292", callback=self.parse_pagination)
        else:
            store_list = response.xpath('.//div[contains(@class,"sabai-entity-bundle-type-directory-listing")]')
            for store in store_list:
                item = ChainItem()
                item['store_number'] = store.xpath('.//@id').extract_first().split('-')[-1]
                # if item['store_number'] in self.store_id:
                #     continue
                self.store_id.append(item['store_number'])
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                item['store_name'] = store.xpath('.//div[@class="sabai-directory-title"]/a/@title').extract_first()
                item['coming_soon'] = "0"
                address = store.xpath('.//span[@class="sabai-googlemaps-address sabai-googlemaps-address-0"]/text()').extract_first().strip()
                addr = usaddress.parse(address)
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
                # pdb.set_trace()
                item['address'] = street
                item['city'] = city
                item['state'] =  state
                item['zip_code'] =  zip_code
                item['address2'] = ''
                item['phone_number'] =  store.xpath('.//span[@itemprop="telephone"]/text()').extract_first()

                item['store_hours'] = ''
                yield item

    def parse_pagination(self, response):
        pdb.set_trace()
        store_list = response.xpath('.//div[contains(@class,"sabai-entity-bundle-type-directory-listing")]')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store.xpath('.//@id').extract_first().split('-')[-1]
            if item['store_number'] in self.store_id:
                    continue
            self.store_id.append(item['store_number'])
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_name'] = store.xpath('.//div[@class="sabai-directory-title"]/a/@title').extract_first()
            item['coming_soon'] = "0"
            address = store.xpath('.//span[@class="sabai-googlemaps-address sabai-googlemaps-address-0"]/text()').extract_first().strip()
            addr = usaddress.parse(address)
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
            # pdb.set_trace()
            item['address'] = street
            item['city'] = city
            item['state'] =  state
            item['zip_code'] =  zip_code
            item['address2'] = ''
            item['phone_number'] =  store.xpath('.//span[@itemprop="telephone"]/text()').extract_first()

            item['store_hours'] = ''
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

