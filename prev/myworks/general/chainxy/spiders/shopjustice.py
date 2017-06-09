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
from lxml import html

class Shopjustice(scrapy.Spider):
    name = "shopjustice"

    domain = "http://www.shopjustice.com/"
    start_urls = ["http://maps.shopjustice.com/api/getAsyncLocations?template=search&level=search&radius=10000&search=New+York%2C+US&_=1495469812889"]
    store_id = []

    def parse(self, response):
        store_list = html.fromstring(json.loads(response.body)['maplist']).xpath('.//li[@class="rio-li"]')
        loc =  json.loads(response.body)['markers']
        for x, store in enumerate(store_list):
            try:
                item = ChainItem()
                item['store_number'] = store.xpath('.//@id')[0].replace('lid', '')
                item['latitude'] = loc[x]['lat']
                item['longitude'] = loc[x]['lng']
                item['store_name'] = store.xpath('.//div[@class="loc-name"]//a/text()')[0]
                item['other_fields'] = ""
                address = store.xpath('.//div[@class="addr em-indent"]/text()')[0] + ' ' + store.xpath('.//div[@class="csz em-indent"]/text()')[0].strip() 
                addr = usaddress.parse(address)
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
                item['country'] = 'United States'
                item['city'] = city
                item['state'] =  state
                item['zip_code'] =  zip_code
                # if zip_code.strip() == '':
                #     pdb.set_trace()
                if zip_code.strip() == '' or zip_code.isdigit() == False:
                    continue
                item['phone_number'] =  store.xpath('.//div[@class="phone em-indent"]/text()')[0].strip()
                hours = store.xpath('.//meta[@itemprop="openingHours"]/@content')
                item['store_hours'] = "; ".join(hours)
                item['coming_soon'] = "0"
          
                yield item
            except:
                pdb.set_trace()
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

