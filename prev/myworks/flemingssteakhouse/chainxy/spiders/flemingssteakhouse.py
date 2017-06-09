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

class Flemingssteakhouse(scrapy.Spider):
    name = "flemingssteakhouse"

    domain = "http://www.flemingssteakhouse.com/"
    start_urls = ["https://www.flemingssteakhouse.com/locations/"]
    store_id = []

    def parse(self, response):
        store_urls = response.xpath('//dl[@class="large-3 columns"]/dd/a/@href').extract()
        for url in store_urls:
            yield scrapy.Request(url='https://www.flemingssteakhouse.com' + url, callback=self.parse_store)
    
    # calculate number of pages
    def parse_store(self, response):
        store_info = response.xpath('//div[@class="location-details alt"]')
        item = ChainItem()

        item['store_number'] = ''
        item['store_name'] = response.xpath('.//h1[@class="headline-maroon"]/text()').extract_first().strip()
        item['address2'] = ''
        address = store_info.xpath('.//address/text()').extract_first().strip()
        item['address'] = "".join(address.split(',')[:-2]).strip()
        item['city'] = address.split(',')[-2].strip()
        item['state'] = address.split(',')[-1].strip().split(' ')[0]
        item['zip_code'] = address.split(',')[-1].strip().split(' ')[1]
            
        item['country'] = 'United States'
        item['phone_number'] = store_info.xpath('.//div[@class="phone-number"]/text()').extract_first().strip()
        item['latitude'] = ''
        item['longitude'] = ''

        hours = store_info.xpath('.//ul/li')
        item['store_hours'] = ''
        for hour in hours:
            try:
                item['store_hours'] += hour.xpath('.//text()').extract_first().replace(u'\u2013', '-') +  hour.xpath('.//time/text()').extract_first().replace(u'\u2013', '-') + "; "
            except:
                pass
        item['other_fields'] = ""
        item['coming_soon'] = "0"
            
        yield item
            





        

