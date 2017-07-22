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

class Rollerz(scrapy.Spider):
    name = "rollerz"

    domain = "http://www.rollerz.com/"
    start_urls = ["http://www.rollerz.com/locator/index.php?brand=r&mode=desktop&pagesize=5&mi_or_km=mi&latitude=38.9273849&longitude=-77.01254449999999&q=20310"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//page-text/div[@class="listing"]')
        for store in store_list:
            script = '{' + store.xpath('.//script/text()').extract_first().split('= {')[1].split('Locator.storeIndexes')[0].strip()[:-1]
            info = json.loads(script)
            item = ChainItem()
            item['store_number'] = info['StoreId']
            item['country'] = 'United States'
            item['latitude'] = info['Latitude']
            item['longitude'] = info['Longitude']
            item['store_name'] = ''
            item['other_fields'] = ""
            if info['StatusName'].find('Coming Soon') != -1:
                item['coming_soon'] = "1"
            else:
                item['coming_soon'] = "0"
            item['address'] = info['Address']
            item['address2'] = ''
            item['city'] = info['City']
            item['state'] = info['State']
            item['zip_code'] = info['Zip']
            item['phone_number'] =  info['Phone']

            item['store_hours'] = ''
            pdb.set_trace()
            for hour in info['StoreHours']:
                item['store_hours'] += hour['Hour'] + '; '
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

