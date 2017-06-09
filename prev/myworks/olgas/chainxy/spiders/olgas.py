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

class Olgas(scrapy.Spider):
    name = "olgas"

    domain = "http://www.olgas.com/"
    start_urls = ["http://www.olgas.com/wp-admin/admin-ajax.php?action=store_search&lat=38.8906038&lng=-90.18427639999999&max_results=100&radius=25000"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.body)
        for store in store_list:
            try:
                item = ChainItem()

                item['store_number'] = store['id']
                item['store_name'] = store['store']
                item['address'] = store['address']
                item['city'] = store['city']
                item['state'] = store['state']
                item['zip_code'] = store['zip']
                
                item['address2'] = store['address2']
                item['country'] = 'United States'

                item['phone_number'] = store['phone']
                item['latitude'] = store['lat']
                item['longitude'] = store['lng']

                item['store_hours'] = "Mon-Fri:" + store['store_time_weekdays'] + "; Sat-Sun:" + store['store_time_weekend']
                item['other_fields'] = ""
                item['coming_soon'] = "0"
            except:
                pdb.set_trace()
            yield item




        

