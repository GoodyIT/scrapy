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

class Rogersandhollands(scrapy.Spider):
    name = "rogersandhollands"

    domain = "https://rogersandhollands.com"
    start_urls = [""]
    store_id = []

    headers = {
        "Accept":"text/javascript, text/html, application/xml, text/xml, */*",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"
    }

    def start_requests(self):
        request_url = "https://rogersandhollands.com/ustorelocator/location/searchJson/"
        form_data = {
            'radius':'20000',
            'lat': '26.1897731',
            'lng': '-80.10377210000001',
            'loc_type':'postal_code'
        }
        yield FormRequest(url=request_url, formdata=form_data, headers=self.headers, callback=self.parse_content)

    def parse_content(self, response):
        store_list = json.loads(response.body)['markers']
        for store in store_list:
            request = scrapy.Request(url=store['website_url'], callback=self.parse_store)
            request.meta['store'] = store
            yield request

    def parse_store(self, response):
        try:
            store = response.meta['store']
            item = ChainItem()
            item['store_number'] = store['location_id']
            item['country'] = 'United States'
            item['latitude'] = store['latitude']
            item['longitude'] = store['longitude']
            item['store_name'] = store['title'].split('-')[0].strip()
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            addr = usaddress.parse(store['address'])
            city = state = zip_code = street = ''
            for temp in addr:
                if temp[1] == 'PlaceName':
                    city += temp[0].replace(',','') + ' '
                elif temp[1] == 'StateName':
                    state = temp[0].replace(',','')
                elif temp[1] == 'ZipCode':
                    zip_code = temp[0].replace(',','')
                else:
                    street += temp[0].replace(',','') + ' '
            item['address'] = self.validate(street)
            item['address2'] = ''
            item['city'] = city
            item['state'] =  state
            item['zip_code'] =  zip_code
            item['phone_number'] =  store['phone']

            item['store_hours'] = ''
            hours  = response.xpath('.//div[@class="locationPageContent"]/table//tr')
            for hour in hours:
                hour = hour.xpath('.//text()').extract()
                hour = [tp.strip().replace('\n', '') for tp in hour if tp.strip() != ""]
                item['store_hours'] += hour[0] + ' ' + hour[1] + "; "
            # hours = response.xpath('.//div[@class="locationPageContent"]/p[1]//text()').extract()
            # item['store_hours'] = "; ".join(hours[3:]).strip()
            yield item
        except:
            pdb.set_trace()
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-').replace(u'\u2013', '-')
        else:
            return ""





        

