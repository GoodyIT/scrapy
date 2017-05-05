import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem

import pdb

class Lennys(scrapy.Spider):
    name = "lennys"

    domain = "http://www.lennys.com/"
    store_id = []

    # calculate number of pages
    def start_requests(self):
        yield scrapy.Request(url='https://www.lennys.com/locations/', headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Cookie':'CFID=59662906; CFTOKEN=31653469; _gat=1; _ga=GA1.2.1230111863.1493822037; _gid=GA1.2.1456468815.1493823274'}, callback=self.parse_state)

    def parse_state(self, response):
        pdb.set_trace()
        state_list=response.xpath('area');
        for state in state_list:
            if state.xpath('.//@href'):
                url = "http://www.lennys.com" + state.xpath('.//@href/text()').extract_first()
                request = scrapy.Request(url=url, callback=self.parse_store_contents)
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

        

