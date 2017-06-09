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

class Plazceplazatireservice(scrapy.Spider):
    name = "plazceplazatireservice"

    domain = "http://www.plazatireservice.com/store-locator/"
    start_urls = ["http://www.plazatireservice.com/wp-content/themes/plazatireservicev2/locations.xml"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//marker')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = store.xpath('.//@lat').extract_first()
            item['longitude'] = store.xpath('.//@lng').extract_first()
            item['store_name'] = self.validate(store.xpath('.//@name').extract_first())
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            item['address'] = store.xpath('.//@address').extract_first()
            item['address2'] = self.validate(store.xpath('.//@address2').extract_first())
            item['city'] = self.validate(store.xpath('.//@city').extract_first())
            item['state'] = store.xpath('.//@state').extract_first()
            item['zip_code'] = store.xpath('.//@postal').extract_first()
            item['phone_number'] =  store.xpath('.//@phone').extract_first()

            item['store_hours'] = self.validate(store.xpath('.//@hours1').extract_first()) + "; "
            if self.validate(store.xpath('.//@hour2').extract_first()) != "":
                item['store_hours'] += self.validate(store.xpath('.//@hours2').extract_first()) + "; "
            if self.validate(store.xpath('.//@hour3').extract_first()) != "":
                item['store_hours'] += self.validate(store.xpath('.//@hours3').extract_first()) + "; "

            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', "'").replace(u'\2013', '-')
        else:
            return ""


            





        

