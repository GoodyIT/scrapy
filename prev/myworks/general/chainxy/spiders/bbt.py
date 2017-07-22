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

class Bbt(scrapy.Spider):
    name = "bbt"

    domain = "https://www.bbt.com/"
    start_urls = ["https://www.bbt.com/locator/"]
    name_list = []

    def __init__(self):
        ca_json = open('citiesusca.json', 'rb')
        self.ca_long_lat_fp = json.load(ca_json)

    def start_requests(self):
        for city in self.ca_long_lat_fp:
            if self.ca_long_lat_fp[city]["country"] == "United States":
                request_url = "https://www.bbt.com/clocator/searchLocations.do?quickZip="+self.ca_long_lat_fp[city]["zip_code"]+"&type=branch&services="
                yield scrapy.Request(url=request_url, callback=self.parse_store)
               # yield scrapy.Request(url="http://www.campbowwow.com/CustomWeb/StoreLocator.asmx/SearchByLocation", headers={"Accept":"*/*","Accept-Encoding":"gzip, deflate", "Content-Type":"application/json; charset=UTF-8", "X-Requested-With":"XMLHttpRequest"}, body=json.dumps('{"strLocation": "98405", "strLat": self.ca_long_lat_fp[city]["latitude"], "strLng": self.ca_long_lat_fp[city]["longitude"], "strRadius": "50"}'), method='post', callback=self.parse_store)

    def parse_store(self, response):
        try:
            store_list = json.loads(response.body)['locationsFound']
            for store in store_list:
                item = ChainItem()
                if store['locationName'] in self.name_list:
                    continue
                self.name_list.append(store['locationName'])
                item['phone_number'] =  store['phone']
                item['store_number'] = store['centerATMNumber']
                item['country'] = 'United States'
                item['latitude'] = store['latitude']
                item['longitude'] = store['longitude']
                item['store_name'] = store['locationName']
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['address'] = store['address1']
                item['address2'] = self.validate(store['address2'])
                item['city'] = store['city']
                item['state'] = store['state']
                item['zip_code'] = store['zip']

                item['store_hours'] = store['lobbyHours'][0] + '; '+ store['lobbyHours'][1] + '; '+  store['lobbyHours'][2] + '; '+  store['lobbyHours'][3] + '; '+  store['lobbyHours'][4] + '; '+  store['lobbyHours'][5] + '; '+ store['lobbyHours'][6] + '; '
                yield item
        except:
            pdb.set_trace()
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-').replace('&#8217;', "'")
        else:
            return ""





        

