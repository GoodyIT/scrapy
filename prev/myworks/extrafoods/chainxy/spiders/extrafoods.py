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

from lxml import html
import pdb

class Extrafoods(scrapy.Spider):
    name = "extrafoods"

    domain = "http://www.extrafoods.ca/"
    start_urls = ["http://www.extrafoods.ca/en_CA/store-list-page.html"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        _response = html.fromstring(response.body.split('<section class="main page-content-full">')[1].strip())
        store_list = _response.xpath('//ul[@class="store-select"]/li/a')
        for store_url in store_list:
            request_url = 'http://www.extrafoods.ca' + store_url.xpath('.//@href')[0]
            request = scrapy.Request(url=request_url, callback=self.parse_city)
            request.meta['state'] = store_url.xpath('.//text()')[0]
            yield request

    def parse_city(self, response):
        _response = html.fromstring(response.body.split('<section class="main page-content-full">')[1].strip())
        city_list = _response.xpath('//ul[@class="store-select"]/li/a/text()')
        for city in city_list:
            request_url = 'http://www.extrafoods.ca/banners/store/v1/listing/extrafoods?lang=en_CA&banner=21&proximity=75&city=%s&province=%s' % (city, response.meta['state'])
            request = scrapy.Request(url=request_url, callback=self.parse_store)
            request.meta['city'] = city
            yield request

    def parse_store(self, response):
        try:
            store_list = json.loads(response.body)
            pdb.set_trace()

            for store_info in store_info_list:    
                item = ChainItem()
                pdb.set_trace()

                item['store_number'] = store_info.xpath('.//@data-store-number').extract_first()
                item['store_name'] = store_info.xpath('.//div[@class="col"]/div[@class="store-info"]/h3/text()').extract_first()
                address = store_info.xpath('.//div[@class="col"]/div[@class="store-address"]/text()').extract()[:-1]
                item['city'] = response.meta['city']
                item['state'] = store_info.xpath('.//@data-store-province').extract_first()
                item['zip_code'] = store_info.xpath('.//@data-postal-code').extract_first()
                item['address'] =  address[0]
                item['address2'] = ''
                item['country'] = 'Canada'
                item['phone_number'] = address[-1]
                item['latitude'] = ''
                item['longitude'] = ''
                hours = store_info.xpath('.//div[@class="col"]/div[@class="store-hours"]/table/tr')
                item['store_hours'] = ''
                for hour in hours:
                    item['store_hours'] += hour.xpath('.//th[1]/text()').extract_first() + ' ' +  hour.xpath('.//th[2]/text()').extract_first()
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                    
                yield item
        except:
            pass
        

    def validate(self, value):
        if type(value) == "str":
            return value
        else:
            return ""





        

