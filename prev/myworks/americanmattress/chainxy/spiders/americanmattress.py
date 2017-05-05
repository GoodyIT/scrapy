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

class Americanmattress(scrapy.Spider):
    name = "americanmattress"

    domain = "http://www.hannaford.com/custserv/locate_store.cmd/"
    start_urls = ["https://www.americanmattress.com/api/Location/GetByCountry"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_list = json.loads(response.body)['Data']
        for store_info in store_list:
            item = ChainItem()

            item['store_number'] = store_info['StoreID']
            item['store_name'] = store_info['Name']
            item['city'] = store_info['City']
            item['state'] = store_info['GeoState']['StateCode']
            item['zip_code'] = store_info['Zip']
            item['address'] = store_info['Street']
            item['address2'] = ''
            item['country'] = 'United States'
            item['phone_number'] = store_info['Phone']
            item['latitude'] = store_info['Latitude']
            item['longitude'] = store_info['Longitude']

            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['store_hours'] = ""
                

            yield item




        

