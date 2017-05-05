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

class Aaronbrothers(scrapy.Spider):
    name = "aaronbrothers"

    domain = "http://www.aaronbrothers.com/"
    start_urls = ["http://www.aaronbrothers.com/store_locator/?zipcode=85250&distance=10000000000&commit=Find"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_list = response.xpath("//table[@class='store-location-results']/tr")
        for store_info in store_list:
            item = ChainItem()

            try:
                item['store_name'] = store_info.xpath(".//td[@style='width:265px']/p[@class='title']/text()").extract_first()
                if item['store_name'] == None:
                    continue

                item['store_number'] = ""
                address = store_info.xpath(".//td[@style='width:265px']/p[@class='location-info']/text()").extract()
                item['address'] = address[0].strip()
                item['address2'] = ''
                item['city'] = address[1].split(',')[0].strip()
                item['state'] = address[1].split(',')[1].strip().split(" ")[0].strip()
                item['zip_code'] = address[1].split(',')[1].strip().split(" ")[1].strip()
                item['country'] = 'United States'
                item['phone_number'] = address[2].strip()
                item['latitude'] = ''
                item['longitude'] = ''

                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['store_hours'] = store_info.xpath(".//location-info").extract_first()
            except:
                pdb.set_trace()  

            yield item




        

