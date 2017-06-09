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

class Bbq(scrapy.Spider):
    name = "bbq"

    domain = "http://mission-bbq.com/"
    start_urls = ["http://mission-bbq.com/locations"]
    store_id = []

    def parse(self, response):
        hours = "; ".join(response.xpath('//div[1][@class="hours"]/p/text()').extract())
        store_list = response.xpath('.//div[contains(@class, "views-accordion-item")]')
        for store_info in store_list:
            item = ChainItem()

            item['store_number'] = ''
            item['store_name'] = store_info.xpath('.//div[@class="views-field-title"]/span[@class="field-content"]/h3/text()').extract_first()
            item['address'] = store_info.xpath('.//div[@class="views-field-street-1"]/span[@class="field-content"]/text()').extract_first()
            item['address2'] = ''
            item['city'] = store_info.xpath('.//div[@class="views-field-address"]/div[@class="field-content"]/div[@class="location vcard"]/div[@class="adr"]/span[@class="locality"]/text()').extract_first()
            item['state'] = store_info.xpath('.//div[@class="views-field-address"]/div[@class="field-content"]/div[@class="location vcard"]/div[@class="adr"]/span[@class="region"]/text()').extract_first()
            item['zip_code'] = store_info.xpath('.//div[@class="views-field-address"]/div[@class="field-content"]/div[@class="location vcard"]/div[@class="adr"]/span[@class="postal-code"]/text()').extract_first()
            item['country'] = 'United States'
            item['phone_number'] = store_info.xpath('.//div[@class="views-field-field-rphone-value"]/span/text()').extract_first().split(' ')[0]

            try:
                loc = store_info.xpath('.//div[@class="views-field-nid"]/span/a[2]/@href').extract_first().split('!8m2!3d')[1].strip()
                item['latitude'] = loc.split('!4d')[0]
                item['longitude'] = loc.split('!4d')[1].split('!3m4')[1]
            except:
                try:
                    loc = store_info.xpath('.//div[@class="views-field-nid"]/span/a[2]/@href').extract_first().split('/@')[1].strip()
                    item['latitude'] = loc.split(',')[0]
                    item['longitude'] = loc.split(',')[1]
                except:
                    item['latitude'] = ''
                    item['longitude'] = ''

            item['store_hours'] = hours
            item['other_fields'] = ""
            item['coming_soon'] = "0"
                
            yield item

    def validate(self, value):
        if type(value) == "str":
            return value
        else:
            return ""





        

