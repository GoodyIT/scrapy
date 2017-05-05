import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem

import pdb
from geopy.geocoders import Nominatim

class Farmershomefurniture(scrapy.Spider):
    name = "farmershomefurniture"

    domain = "http://www.farmershomefurniture.com/"
    start_urls = ["http://farmershomefurniture.com/store-list"]
    store_id = []

    def __init__(self):
        self.geolocator = Nominatim()

    # calculate number of pages
    def parse(self, response):
        store_list=response.xpath('.//*[@id="content-container"]/div[3]/div/table/tbody/tr');
        for store_info in store_list:
            item = {}
            item['store_number'] = store_info.xpath(".//td/text()")[0].extract()
            item['city'] = store_info.xpath(".//td/text()")[1].extract()
            item['state'] = store_info.xpath(".//td/text()")[2].extract()
            item['address'] = store_info.xpath(".//td/text()")[3].extract()
            item['phone_number'] = store_info.xpath(".//td/text()")[4].extract()
            url = self.domain + store_info.xpath('./@onclick').extract_first()[26:]
            request = scrapy.Request(url=url, callback=self.parse_store_contents)
            request.meta['store_number'] = item['store_number'];
            request.meta['city'] = item['city']
            request.meta['state'] = item['state']
            request.meta['address'] = item['address']
            request.meta['phone_number'] = item['phone_number']
            yield request

    # pare store detail page
    def parse_store_contents(self, response): 
        pdb.set_trace()

        store = response.xpath("//div[contains(@class, 'contact_information BasicInfo-BS')]")
        item = ChainItem()
        
        item['store_name'] = ''
        item['store_number'] = response.meta["store_number"]
        address = store.xpath("//p[contains(@class, 'Address')]/text()").extract()
        item['address'] = response.meta["address"]
        item['address2'] = ''
        item['phone_number'] = response.meta["phone_number"]
        item['city'] = response.meta["city"]
        item['state'] = response.meta["state"]
        item['country'] = 'United States'
        item['city'] = response.meta["city"]
        item['latitude'] = response.meta["lat"]
        item['longitude'] = response.meta["lng"]
       
        item['zip_code'] = location.raw["address"]["postcode"]
        
        item['store_hours'] = self.validate(store.xpath(".//dd/text()"))
        
        #item['store_type'] = info_json["@type"]
        item['other_fields'] = ""
        item['coming_soon'] = "0"

        yield item

    def validate(self, xpath_obj):
        
        try:
            return xpath_obj.extract_first().strip()
        except:
            return ""

        

