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

class O2fitnessclubs(scrapy.Spider):
    name = "o2fitnessclubs"

    domain = "http://www.o2fitnessclubs.com/"
    start_urls = ["http://www.o2fitnessclubs.com/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//div[contains(@class, "location-container")]/ul/li/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse_store)

    def parse_store(self, response):
        item = ChainItem()

        item['store_number'] = ''
        item['store_name'] = response.xpath('.//h2[@class="location-name"]/span[2]/text()').extract_first().replace(u'\u2013', '-')
        item['address'] = response.xpath('.//span[@itemprop="streetAddress"]/strong/text()').extract_first()
        item['address2'] = ''
        item['city'] = self.validate(response.xpath('.//span[@itemprop="addressLocality"]/text()').extract_first())
        item['state'] = response.xpath('.//span[@itemprop="addressRegion"]/text()').extract_first()
        item['zip_code'] = response.xpath('.//span[@itemprop="postalCode"]/text()').extract_first()
        item['country'] = 'United States'

        item['phone_number'] = response.xpath('.//h2[@class="location-name"]/span[@itemprop="telephone"]/span/a/text()').extract_first().split(' ')[0]
        item['latitude'] = ''
        item['longitude'] = ''

        item['store_hours'] = ''
        try:
            item['store_hours'] = response.xpath('.//div[@itemprop="department"]/time[1]/time[1]/strong/text()').extract_first() + "".join(response.xpath('.//div[@itemprop="department"]/time[1]/time[1]/text()').extract())
        except:
            try:
                item['store_hours'] = response.xpath('.//time[@itemprop="openingHours"]/strong/text()').extract_first() + response.xpath('.//time[@itemprop="openingHours"]/text()').extract_first()
            except:
                item['store_hours'] = response.xpath('.//time[@itemprop="openingHours"]/text()').extract_first()

        item['store_hours'] = item['store_hours'].encode('utf8').replace('\xe2\x80\x93', '-').replace('\n', '')
        item['other_fields'] = ""
        item['coming_soon'] = "0"
            
        yield item

    def validate(self, value):
        if value == None:
            return ""
        else:
            return value





        

