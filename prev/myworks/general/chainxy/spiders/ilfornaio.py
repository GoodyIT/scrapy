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

class Ilfornaio(scrapy.Spider):
    name = "ilfornaio"

    domain = "http://www.ilfornaio.com"
    start_urls = ["http://www.ilfornaio.com/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//div[@class="super_nav"]/li/ul/li/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url=self.start_urls[0] + url, callback=self.parse_store)

    def parse_store(self, response):
        item = ChainItem()
        store = response.xpath('.//div[@id="MapDescription"]')
        item['store_number'] = ''
        
        left = response.xpath('.//div[@class="info_left"]')
        item['store_name'] = self.validate(left.xpath('.//header//text()').extract_first())
        address = left.xpath('.//header/p//text()').extract()
        address = [tp.strip() for tp in address if tp.strip() != ""]
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
        item['phone_number'] = left.xpath(".//div[contains(@class, 'contact_info')]/p[1]/a/text()").extract_first().replace('P:', '').strip()

        item['latitude'] = ''
        item['longitude'] = ''
        item['store_hours'] = ''
        item['store_hours'] = "; ".join(response.xpath("//div[contains(@class, 'hours')]/p/text()").extract())
        item['other_fields'] = ""
        item['coming_soon'] = "0"
        yield item

    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2013', '-').replace(u'\u2019', "'").replace('&#039;', '')
        else:
            return ""





        

