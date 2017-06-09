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

class Savemart(scrapy.Spider):
    name = "savemart"

    domain = "https://www.savemart.com/"
    start_urls = ["https://savemart.myrelationshop.com/Sysnify.Relationshop.v2/StoreLocation/SearchStore"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.body.split('<script type=\'text/javascript\'>\r\n    var stores = ')[1].strip().split(';\r\n ')[0].strip())
        for store_info in store_list:
            item = ChainItem()

            item['store_number'] = store_info['CS_StoreID']
            item['store_name'] = store_info['StoreName']
            item['address'] = store_info['Address1']
            item['address2'] = store_info['Address2']
            item['city'] = store_info['City']
            item['state'] = store_info['State']
            item['zip_code'] = store_info['Zipcode']
            item['country'] = 'United States'
            item['phone_number'] = store_info['PhoneNumber']
            item['latitude'] = store_info['Latitude']
            item['longitude'] = store_info['Longitude']
            item['store_hours'] = store_info['StoreHours']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
                
            yield item

    def validate(self, value):
        if type(value) == "str":
            return value
        else:
            return ""





        

