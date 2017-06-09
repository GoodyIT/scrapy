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

class Salsaritas(scrapy.Spider):
    name = "salsaritas"

    domain = "http://www.salsaritas.com/"
    start_urls = ["http://salsaritas.com/wp-content/themes/Salsaritas/superstorefinder/index.php"]
    store_id = []

    def start_requests(self):
        yield FormRequest(url="http://salsaritas.com/wp-content/themes/Salsaritas/superstorefinder/index.php", headers={"Content-Type": "application/x-www-form-urlencoded"},
                    formdata={"ajax":"1", "action":"get_nearby_stores", "distance":"3000", "lat":"39.989813","lng":"-98.505488", "products":"null", "catlist":""},
                    callback=self.parse_store)
    # calculate number of pages
    def parse_store(self, response):
        store_list = json.loads(response.body.replace('\xef\xbb\xbf\n\n', ''))['stores']
        for store_info in store_list:
            item = ChainItem()

            item['store_number'] = ''
            item['store_name'] = store_info['name']
            item['address2'] = ''
            if len(store_info['address'].split(',')) == 2:
                if len(store_info['address'].split(',')[-1].strip().split(' ')) == 2:
                    item['address'] = " ".join(store_info['address'].split(',')[0].strip().split(' ')[:-1])
                    item['city'] = store_info['address'].split(',')[0].strip().split(' ')[-1]
                    item['state'] = store_info['address'].split(',')[-1].strip().split(' ')[0]
                    item['zip_code'] = store_info['address'].split(',')[-1].strip().split(' ')[1]
                else:
                    item['address'] = store_info['address'].split(',')[0].strip()
                    item['city'] = store_info['address'].split(',')[-1].strip().split(' ')[0]
                    item['state'] = store_info['address'].split(',')[-1].strip().split(' ')[1]
                    item['zip_code'] = store_info['address'].split(',')[-1].strip().split(' ')[2]
            elif len(store_info['address'].split(',')) == 3:
                item['address'] = store_info['address'].split(',')[0].strip()
                item['city'] = store_info['address'].split(',')[1].strip()
                item['state'] = store_info['address'].split(',')[-1].strip().split(' ')[0]
                item['zip_code'] = store_info['address'].split(',')[-1].strip().split(' ')[1]
            elif len(store_info['address'].split(',')) == 4:
                item['address'] = store_info['address'].split(',')[0].strip()
                item['address2'] = store_info['address'].split(',')[0].strip()
                item['city'] = store_info['address'].split(',')[-2].strip()
                item['state'] = store_info['address'].split(',')[-1].strip().split(' ')[0]
                item['zip_code'] = store_info['address'].split(',')[-1].strip().split(' ')[1]
            else:
                item['address'] = store_info['address'].split(',')[0].strip()
                item['city'] = store_info['address'].split(',')[1].strip().split(' ')[0]
                item['state'] = store_info['address'].split(',')[-1].strip().split(' ')[1]
                item['zip_code'] = store_info['address'].split(',')[-1].strip().split(' ')[2]
            try:
                l = int(item['zip_code'])
            except:
                item['zip_code'] = ''
            item['country'] = 'United States'
            item['phone_number'] = store_info['telephone']
            item['latitude'] = store_info['lat']
            item['longitude'] = store_info['lng']
            item['store_hours'] = ''
            item['other_fields'] = ""
            item['coming_soon'] = "0"
                
            yield item

    def validate(self, value):
        if type(value) == "str":
            return value
        else:
            return ""





        

