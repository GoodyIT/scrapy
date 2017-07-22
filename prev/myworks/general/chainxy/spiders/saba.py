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

class Saba(scrapy.Spider):
    name = "saba"

    domain = "https://www.sabas.com/"
    start_urls = ["https://www.sabas.com/locations"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//div[@id="System_8vAx9XTY"]/div[@class="tb_text_wrap"]//text()').extract()
        store_list = [tp.strip().replace('\n', '') for tp in store_list if tp.strip() != ""]

        store = []
        for x in xrange(0,len(store_list)):
            info = store_list[x]
            result = re.findall(r'\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}', info)
            if result:
                store.append(info)
                item = ChainItem()
                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                item['store_name'] = self.validate(store[0])
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['address2'] = ''
                addr = usaddress.parse(store[1])
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
                item['city'] = city
                item['state'] =  state
                item['zip_code'] =  zip_code
                item['phone_number'] =  store[2]

                item['store_hours'] = ''
                store = []
                yield item
            else:
                store.append(info)
            
      
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\xa0', u' ')
        else:
            return ""





        

