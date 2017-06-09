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

class Campbowwow(scrapy.Spider):
    name = "campbowwow"

    domain = "http://www.campbowwow.com/"
    start_urls = ["http://www.campbowwow.com//location?location=98405"]
    store_name = []
    phone_number = []

    def __init__(self):
        ca_json = open('citiesusca.json', 'rb')
        self.ca_long_lat_fp = json.load(ca_json)

    def start_requests(self):
        request_url = "http://www.campbowwow.com/CustomWeb/StoreLocator.asmx/SearchByLocation"
        for city in self.ca_long_lat_fp:
            if self.ca_long_lat_fp[city]["country"] == "United States":
                header={
                    "Accept":"*/*",
                    "Accept-Encoding":"gzip, deflate",
                    "Content-Type":"application/json; charset=UTF-8",
                    "X-Requested-With":"XMLHttpRequest"
                }

                payload = {
                    "strLat":float(self.ca_long_lat_fp[city]["latitude"]),
                    "strLng":float(self.ca_long_lat_fp[city]["longitude"]),
                    "strLocation":self.ca_long_lat_fp[city]["zip_code"],
                    "strRadius":"50"
                }
                yield scrapy.Request(url=request_url, headers=header, body=json.dumps(payload), method="post", callback=self.parse_store)
               # yield scrapy.Request(url="http://www.campbowwow.com/CustomWeb/StoreLocator.asmx/SearchByLocation", headers={"Accept":"*/*","Accept-Encoding":"gzip, deflate", "Content-Type":"application/json; charset=UTF-8", "X-Requested-With":"XMLHttpRequest"}, body=json.dumps('{"strLocation": "98405", "strLat": self.ca_long_lat_fp[city]["latitude"], "strLng": self.ca_long_lat_fp[city]["longitude"], "strRadius": "50"}'), method='post', callback=self.parse_store)

    def parse_store(self, response):
        try:
            store_list = json.loads(str(json.loads(response.body)['d']))['Results']
            for store in store_list:
                item = ChainItem()
                if len(store['Address'].split('|')) >= 3 and store['Address'].split('|')[-1].find('-') != -1:
                    item['phone_number'] = self.validate(store['Address'].split('|')[-1])
                    if item['phone_number'] in self.phone_number:
                        continue
                    self.phone_number.append(item['phone_number'])

                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = store['Lat']
                item['longitude'] = store['Long']
                item['store_name'] = self.validate(store['Title'])
                if item['store_name'] in self.store_name:
                    continue
                self.store_name.append(item['store_name'])

                # if item['store_name'].find('Fort Worth West') != -1:
                #     pdb.set_trace()

                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['address2'] = ''
                item['address'] = ''
                # if store['Address'].find('Swansea, Illinois 62226') != -1:
                #     pdb.set_trace()

                if len(store['Address'].strip().split('|')) == 1:
                    parse_citystatezip = self.parse_citystatezip(store['Address'])
                    item['city'] = parse_citystatezip[0]
                    item['state'] = parse_citystatezip[1]
                    item['zip_code'] = parse_citystatezip[2]
                elif len(store['Address'].strip().split('|')) == 2 and store['Address'].strip().split('|')[0] == '' or len(store['Address'].strip().split('|')) == 1:
                    item['address'] = ''
                    if store['Address'].strip()[-1].isdigit():
                        item['address'] =  ''
                        parse_citystatezip = self.parse_citystatezip(store['Address'].strip().split('|')[-1])
                        item['city'] = parse_citystatezip[0]
                        item['state'] = parse_citystatezip[1]
                        item['zip_code'] = parse_citystatezip[2]
                    else:
                        address = store['Address'].split('|')[-1].split(',')
                        item['city'] = address[0].strip()
                        item['state'] =  address[1].strip()
                else:
                    if len(store['Address'].strip().split('|')) == 3:
                        if store['Address'].split('|')[-1].find('-') != -1 or store['Address'].split('|')[-1].find(')') != -1:
                            item['address'] = ' '.join(store['Address'].split('|')[:-2])
                            address = store['Address'].split('|')[-2]
                        else:
                            item['address'] = ' '.join(store['Address'].split('|')[:-1])
                            address =  store['Address'].split('|')[-1]
                    elif len(store['Address'].strip().split('|')) == 4:
                        item['address'] = store['Address'].split('|')[0]
                        if store['Address'].split('|')[-3].find('Suite') != -1 or store['Address'].split('|')[-3].find(',') == -1:
                            address = store['Address'].split('|')[-2]
                        else:
                            address = store['Address'].split('|')[-3]
                    elif len(store['Address'].strip().split('|')) == 2:
                        item['address'] = ' '
                        address = self.validate(store['Address'].split('|')[0]) 
                    else:
                        address = store['Address'].strip()

                    parse_citystatezip = self.parse_citystatezip(address)
                    item['city'] = parse_citystatezip[0]
                    item['state'] = parse_citystatezip[1]
                    item['zip_code'] = parse_citystatezip[2]
                item['store_hours'] = ''
                yield item
        except:
            pdb.set_trace()
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-').replace('&#8217;', "'")
        else:
            return ""

    def parse_citystatezip(self, value):
        city = self.validate(value.split(',')[0])
        state = self.validate(value.split(',')[1].strip().split(' ')[0])
        zip_code = self.validate(value.split(',')[1].strip().split(' ')[-1])
        return (city, state, zip_code)





        

