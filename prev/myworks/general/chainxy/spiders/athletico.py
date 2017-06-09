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

class athletico(scrapy.Spider):
    name = "athletico"

    domain = "http://www.athletico.com/"
    start_urls = ["http://www.athletico.com/search-locations/?address=94203&lat=&lng=&service=&insurance=&language=&submitted=submitted"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//table[@id="locations-table"]/tbody/tr')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_name'] = store.xpath('.//td[1]/a/text()').extract_first()
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            info = store.xpath('.//td[1]/text()').extract()
            info = [tp.strip().replace('\n', '') for tp in info if tp.strip() != ""]
            addr = usaddress.parse(" ".join(info[:2]))
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
            item['address'] = street
            item['city'] = city
            item['state'] =  state
            item['zip_code'] =  zip_code
            item['address2'] = ''
            item['phone_number'] =  info[2]

            item['store_hours'] = ''
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

