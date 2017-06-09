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

class Biscuitscafe(scrapy.Spider):
    name = "biscuitscafe"

    domain = "http://biscuitscafe.com/"
    start_urls = ["http://biscuitscafe.com/locations/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//ul[@id="menu-main-navigation-1"]/li[3]/ul/li/a/@href').extract()
        for url in url_list:
            if url.find('http://biscuitscafe.com/team/oregon/') != -1:
                yield scrapy.Request(url= "http://biscuitscafe.com/wp-admin/admin-ajax.php?action=store_search&lat=45.505237&lng=-122.41296&max_results=25&radius=50&autoload=1", callback=self.parse_oergon_store)
            else:    
                yield scrapy.Request(url= url, callback=self.parse_store)
    
    def parse_oergon_store(self, response):
        store_list = json.loads(response.body)
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store['id']
            item['country'] = 'United States'
            item['latitude'] = store['lat']
            item['longitude'] = store['lng']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['store_hours'] = store['hours']
            item['store_name'] = store['store']
            item['address'] = store['address']
            item['address2'] = ''
            item['city'] = store['city']
            item['state'] = store['state']
            item['zip_code'] = store['zip']
            item['phone_number'] =  store['address2'].replace('Phone:', '').strip()
            yield item
    
    def parse_store(self, response):
        store_list = response.xpath(".//div[@id='pageContent']//text()").extract()
        store_list = [tp.strip().replace('\n', '') for tp in store_list if tp.replace('\n', '').strip() != ""]
        
        store = []
        skip = -10
        for x, value in enumerate(store_list):
            if x == skip + 1 or x == skip + 2:
                continue

            if value.find('Find us in Washington') != -1:
                continue
            if value.find('Select here for directions.') != -1:
                continue
            if value.find('Order Food Delivery with DoorDash') != -1:
                continue
            
            if value.find('Phone') != -1:
                skip = x
                item = ChainItem()
                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['store_name'] = self.validate(store[0])
                addr = usaddress.parse(" ".join(store[1:]))
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
                item['country'] = 'United States'
                item['phone_number'] = store_list[x+1]
                item['store_hours'] = ''
                days = response.xpath(".//div[@id='text-10']/div[contains(@class, 'textwidget')]/strong/text()").extract()
                hours = response.xpath(".//div[@id='text-10']/div[contains(@class, 'textwidget')]/span/text()").extract()
                for x, hour in enumerate(hours):
                    item['store_hours'] += days[x] + ' ' + hour + "; "
                yield item

                store = []
            else:
                skip = -10
                store.append(value)

    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

