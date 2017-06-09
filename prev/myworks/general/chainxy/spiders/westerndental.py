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

class Westerndental(scrapy.Spider):
    name = "westerndental"

    domain = "https://www.westerndental.com/"
    start_urls = ["https://www.westerndental.com/"]
    store_id = []

    def start_requests(self):
        for x in xrange(0,1000,200):
            yield scrapy.Request(url="https://www.westerndental.com/Umbraco/Api/LocationApi/Locations?language=en-US&filterTypes=&latitude=33.6694444&longitude=-117.8222222&locationId=&city=&state=&take=200&skip=%s&radius=1000&sortOrder=Distance" % x, callback=self.parse_store)

    def parse_store(self, response):
        store_list = json.loads(response.body.split('<string xmlns="http://schemas.microsoft.com/2003/10/Serialization/">')[1].strip().split('</string>')[0])['LocationsInfo']
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store['Id']
            item['country'] = 'United States'
            item['latitude'] = store['LatLng']['Latitude']
            item['longitude'] = store['LatLng']['Longitude']
            item['store_name'] = 'WESTERN DENTAL - ' + store['City']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store['Name']
            item['address2'] = ''
            item['city'] = store['City']
            item['state'] = store['StateAbbr']
            item['zip_code'] = store['ZocDocId']
            item['phone_number'] =  self.validate(store['Phone'])

            item['store_hours'] = ''
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-').replace(u'\u2013', '-')
        else:
            return ""





        

