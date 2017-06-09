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

class Volkswagen(scrapy.Spider):
    name = "volkswagen"

    domain = "http://www.volkswagen.com/"
    start_urls = ["http://www.vw.com/vwsdl/rest/product/dealers/box/-29.042961477291264,146.90472778320316_77.77543666245404,46.18207153320304.json?max=900"]
    store_id = []

    def parse(self, response):
        store_list = json.loads(response.body)
        for store in store_list:
            item = ChainItem()
            item['store_number'] = store['dealerid']
            item['country'] = store['country']
            item['latitude'] = store['latlong'].split(',')[0]
            item['longitude'] =store['latlong'].split(',')[1]
            item['store_name'] = store['name']
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store['address1']
            item['address2'] = store['address2']
            item['city'] = store['city']
            item['state'] = store['state']
            item['zip_code'] = store['postalcode']
            item['phone_number'] =  store['phone']

            item['store_hours'] = ''
            # pdb.set_trace()
            try:
                hours = store['hours'][0]['departmentHours']
                for hour in hours:
                    if hour['isClosed'] == 'Y':
                        item['store_hours'] += hour['dayText'] + ':' + 'closed; '
                    else:
                        item['store_hours'] += hour['dayText'] + ':' + hour['openHour'] + '-' + hour['closeHour'] + '; '
            
            except:
                pass
            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

