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

class Fallasstores(scrapy.Spider):
    name = "fallasstores"

    domain = "http://www.fallasstores.com/"
    start_urls = ["http://aws002.basiclink.com/~locatorfallassto/dist/data/locations.xml?origLat=40.71&origLng=-74.00999999999999&origAddress=10292"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_list = response.xpath('//marker')
        for store_info in store_list:
            item = ChainItem()

            item['store_number'] = store_info.xpath('.//@name').extract_first().split('#')[1].strip()
            item['store_name'] = store_info.xpath('.//@name').extract_first()
            item['city'] = store_info.xpath('.//@city').extract_first()
            item['state'] = store_info.xpath('.//@state').extract_first()
            item['zip_code'] = store_info.xpath('.//@postal').extract_first()
            item['address'] = store_info.xpath('.//@address').extract_first()
            item['address2'] = store_info.xpath('.//@address2').extract_first()
            item['country'] = 'United States'
            item['phone_number'] = store_info.xpath('.//@phone').extract_first()
            item['latitude'] = store_info.xpath('.//@lat').extract_first()
            item['longitude'] = store_info.xpath('.//@lng').extract_first()
            
            item['store_hours'] = ''
            # item['store_hours'] = store_info.xpath('.//@hours1').extract_first() + ";" + store_info.xpath('.//@hours2').extract_first()+ ";" + store_info.xpath('.//@hours3').extract_first()+ ";"
            item['other_fields'] = ""
            item['coming_soon'] = "0"
                
            yield item






        

