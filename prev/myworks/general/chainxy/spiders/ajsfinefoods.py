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
from lxml import html

class Ajsfinefoods(scrapy.Spider):
    name = "ajsfinefoods"

    domain = "https://www.ajsfinefoods.com/"
    start_urls = ["https://www.ajsfinefoods.com/wp-admin/admin-ajax.php?action=store_search&lat=33.510039&lng=-112.071731&max_results=25&radius=50&autoload=1"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.body)
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store['id']
            item['country'] = 'United States'
            item['latitude'] = store['lat']
            item['longitude'] = store['lng']
            item['store_name'] = store['store']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store['address']
            item['address2'] = store['address2']
            item['city'] = store['city']
            item['state'] = store['state']
            item['zip_code'] = store['zip']
            item['phone_number'] =  store['phone']

            item['store_hours'] = 'Mon-Sun: 6AM-9PM'
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

