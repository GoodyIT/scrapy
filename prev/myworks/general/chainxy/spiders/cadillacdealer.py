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

class Cadillacdealer(scrapy.Spider):
    name = "cadillacdealer"

    domain = "http://www.cadillacdealer.com"
    phones = []

    def __init__(self):
        us_json = open('citiesusca.json', 'rb')
        self.us_long_lat_fp = json.load(us_json)

    def start_requests(self):
        asdfasdfasdf
        url = "http://www.cadillacdealer.com/InventoryListing?0-1.IFormSubmitListener-border-border_body-virtualVehicleComponentsContainer-locationSelection-updateLocationForm&make=cadillac&pageTypeName=InventoryListing"
        for city in self.us_long_lat_fp:
            if self.us_long_lat_fp[city]["country"] == "United States":
                formdata = {"radius":"100", "zipCode":str(self.us_long_lat_fp[city]['zip_code'])}
                yield FormRequest(url=url, formdata=formdata, callback=self.parse_store)
    
    def parse_store(self, response):
        store_link = response.xpath('.//div[@class="vehicle-summary"]//a[contains(@class,"vehicle-dealer-details-link")]/@href').extract()
        for store in store_link:
            yield scrapy.Request(url=store, callback=self.parse_content)

    def parse_content(self, response):
        item = ChainItem()
        item['store_name'] = self.validate(response.xpath('.//h2[@itemprop="name"]/text()').extract_first())
        pdb.set_trace()
        if (item['store_name'] == ''):
            print '============= name =================== '
            return
        item['phone_number'] = self.validate(response.xpath('.//span[@itemprop="telephone"]/text()').extract_first())
        if item['phone_number'] in self.phones:
            print '============= phone =================== '
            return
        self.phones.append(item['phone_number'])

        print '**********'
        print self.phones
        print '**********'
        
        item['store_number'] = ''
        item['country'] = 'United States'
        item['latitude'] = ''
        item['longitude'] = ''
        item['other_fields'] = ""
        item['coming_soon'] = "0"
        item['address'] = response.xpath('.//span[@if="site.dealer.departments.sales.address.street1"]/text()').extract_first()
        item['address2'] = ''
        item['city'] = response.xpath('.//span[@itemprop="addressLocality"]/text()').extract_first()
        item['state'] = response.xpath('.//span[@itemprop="addressRegion"]/text()').extract_first()
        item['zip_code'] = response.xpath('.//span[@itemprop="postalCode"]/text()').extract_first()

        item['store_hours'] = ''

        yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

