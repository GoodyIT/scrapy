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

class Henribendel(scrapy.Spider):
    name = "henribendel"

    domain = "http://www.henribendel.com/"
    start_urls = ["http://www.henribendel.com/on/demandware.store/Sites-HB-Site/default/Stores-Find"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//table[@class="storelocator storelocator-desktop"]//tr[@class="tablerow"]')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_name'] = store.xpath('.//div[@class="storeinformation"]/p/strong/text()').extract_first()
            item['other_fields'] = ""
            
            item['coming_soon'] = "0"
            address = store.xpath('.//div[@class="storeaddress"]/text()').extract()
            address = [tp.strip().replace('\n', '') for tp in address if tp.strip() != ""]
            addr = usaddress.parse(" ".join(address).replace('United States', '').strip())
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
            # if item['address'].find('160 Walt Whitman Road') != -1:
            #     pdb.set_trace()
            item['phone_number'] =  store.xpath('.//td[@class="storemap"]/p/text()').extract_first()

            hours = store.xpath('.//td[@class="storehours"]/p/strong/text()').extract()
            hours = [tp.strip().replace('\n', '') for tp in hours if tp.strip() != ""]
            item['store_hours'] = "; ".join(hours)
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

