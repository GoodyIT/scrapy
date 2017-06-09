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

class Acerenttoown(scrapy.Spider):
    name = "acerenttoown"

    domain = "https://www.acerenttoown.com/"
    start_urls = ["https://www.acerenttoown.com/index.php?mact=Locations,cntnt01,searchresults,0&cntnt01showtemplate=false&cntnt01returnid=44&cntnt01zipcode=&cntnt01city=&cntnt01state=IA"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.body)
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store['id']
            item['country'] = 'United States'
            item['latitude'] = store['latitude']
            item['longitude'] = store['longitude']
            item['store_name'] = store['name']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store['address']
            item['address2'] = self.validate(store['address2'])
            item['city'] = store['city']
            item['state'] = store['state']
            item['zip_code'] = store['zipcode']
            item['phone_number'] =  store['phone']

            item['store_hours'] = ''
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

