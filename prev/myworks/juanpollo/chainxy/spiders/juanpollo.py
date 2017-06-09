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

class Juanpollo(scrapy.Spider):
    name = "juanpollo"

    domain = "http://www.juanpollo.com/"
    start_urls = ["http://juanpollo.com/wp-admin/admin-ajax.php?action=store_search&lat=34.12427&lng=-117.32051200000001&max_results=25&radius=50&autoload=1"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.body)
        for store_info in store_list:
            item = ChainItem()

            item['store_number'] = store_info['id']
            item['store_name'] = store_info['store']
            item['city'] = store_info['city']
            item['state'] = store_info['state']
            item['zip_code'] = store_info['zip']
            item['address'] = store_info['address']
            item['address2'] = store_info['address2']
            item['country'] = 'United States'
            item['phone_number'] = store_info['phone']
            index = item['store_name'].find(item['phone_number'])
            if index != -1:
                item['store_name'] = item['store_name'][:index]
            item['store_name'] = re.compile(r'\d+').split(item['store_name'])[0].strip()
            item['latitude'] = store_info['lat']
            item['longitude'] = store_info['lng']

            item['store_hours'] = store_info['hours'].replace('<p>', '').replace('</p>', '').replace('<br />', '').replace('\n', ' ').replace('Hours:', '').strip()
            item['other_fields'] = ""
            item['coming_soon'] = "0"
                
            yield item


    def validate(self, value):
        if type(value) == "str":
            return value
        else:
            return ""




        

