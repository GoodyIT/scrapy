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

class Dentalworks(scrapy.Spider):
    name = "dentalworks"

    domain = "https://dentalworks.com/"
    start_urls = ["https://dentalworks.com/Location-Finder"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//div[@class="action-links"]/div[1]//a/@href').extract()
        for url in url_list:
            if url.strip() != '':
                yield scrapy.Request(url=url, callback=self.parse_store)
        
    def parse_store(self, response):
        try:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_name'] = self.validate(response.xpath('.//h1[@class="headline"]/text()').extract_first())
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = response.xpath('.//span[@itemprop="streetAddress"]/text()').extract_first()
            item['city'] = response.xpath('.//span[@itemprop="addressLocality"]/text()').extract_first()
            item['state'] =  response.xpath('.//span[@itemprop="addressRegion"]/text()').extract_first()
            item['zip_code'] =  response.xpath('.//span[@itemprop="postalCode"]/text()').extract_first()
            item['address2'] = ''
            item['phone_number'] = response.xpath('.//a[@itemprop="telephone"]/text()').extract_first()
            hours = response.xpath('.//table[@itemprop="openingHoursSpecification"]//tr')
            item['store_hours'] = ''
            for hour in hours:
                item['store_hours'] +=  self.validate(hour.xpath('.//td[@class="hours-table-left-col"]/text()').extract_first()) + ' '+ self.validate(hour.xpath('.//td[@class="hours-table-right-col"]/time/text()').extract_first()) + "; " 

            yield item
        except:
            pdb.set_trace()
        
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-').replace(u'\u2013', '-')
        else:
            return ""





        

