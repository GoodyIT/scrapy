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

class Pancheros(scrapy.Spider):
    name = "pancheros"

    domain = "http://www.pancheros.com/"
    start_urls = ["https://www.pancheros.com/index.php?ACT=23&locate_method=json&lat=39.1168531&lng=-95.00007690000001&radius=10000"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_list = json.loads(response.body)
        for store_info in store_list:
            item = ChainItem()

            item['store_number'] = store_info['id']
            item['store_name'] = store_info['title']
            item['address2'] = ''
            address1 = ''
            if store_info['store_address'].find('<br />') != -1:
                address = store_info['store_address'].split('<br />')
            else:
                address = store_info['store_address'].split('</p>\n<p>')
            if len(address) == 3:
                item['address'] = self.validate(address[0])
                item['address2'] = self.validate(address[1])
                address1 = address[2].split(' ')
            else:
                item['address'] = self.validate(address[0])
                address1 = address[1].split(' ')

            if len(address1) == 4:
                item['city'] = self.validate(address1[0]) + ' ' + self.validate(address1[1])
                item['state'] = self.validate(address1[2])
                item['zip_code'] = self.validate(address1[3])
            else:
                item['zip_code'] = self.validate(address1[2])
                try:
                    val = int(item['zip_code'])
                    item['city'] = self.validate(address1[0])
                    item['state'] = self.validate(address1[1])
                    if address1[1].find(',') != -1:
                        if address1[1].split(',')[1] == '':
                            item['city'] = self.validate(address1[0]+ ' ' + address1[1])
                            item['state'] = ''
                        else:
                            item['city'] = self.validate(address1[0]) + ' ' + self.validate(address1[1].split(',')[0])
                            item['state'] = address1[1].split(',')[1]
                except ValueError:
                    item['city'] = self.validate(address1[0]) + ' ' + self.validate(address1[1])
                    item['state'] = self.validate(address1[2])
                    item['zip_code'] = ''
                
            item['country'] = 'United States'
            item['phone_number'] = store_info['store_telephone']
            item['latitude'] = store_info['lat']
            item['longitude'] = store_info['lng']

            item['store_hours'] = self.validate(store_info['store_hours']).replace('<br />', '')
            item['other_fields'] = ""
            item['coming_soon'] = "0"
                
            yield item

    def validate(self, value):
        return value.replace('<p>', '').replace('</p>', '').replace('&nbsp;', '').replace(',', '').strip()





        

