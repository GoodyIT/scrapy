import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class WegmansSpider(scrapy.Spider):
    name = "wegmans"
    uid_list = []

    headers = {}

    def __init__(self):
			content = ""
			with open("all_zips") as f:
				content = f.readlines()
			# you may also want to remove whitespace characters like `\n` at the end of each line
			self.zip_code_list = [x.strip() for x in content]
    
    def start_requests(self):
        for zip_code in self.zip_code_list:
            request_url = "https://sp1004f27d.guided.ss-omtrdc.net/?q=*&do=location-search&sp_q_location_1=%s&sp_x_1=zip&sp_q_max_1=1000&sp_s=zip_proximity;sp_c=1000;callback=angular.callbacks._2" % (zip_code)  
            yield scrapy.Request(url=request_url, callback=self.parse_store)

    # get longitude and latitude for a state by using google map.
    def parse_store(self, response):
    	# try:
			stores = json.loads('{' + response.body.split('( {')[1].split('} )')[0] + '}')["results"]

			for store in stores:
				item = ChainItem()
				item['store_name'] = self.validate(store, 'name')
				item['store_number'] = self.validate(store, 'locationNumber')
				item['address'] = self.validate(store, 'address') 
				item['address2'] = self.validate(store, 'address2')
				item['phone_number'] = self.validate(store, 'phone')
				item['city'] = self.validate(store, 'city')
				item['state'] = self.validate(store, 'state')
				item['zip_code'] = self.validate(store, 'zip')
				item['country'] = 'US'
				item['latitude'] = self.validate(store, 'location').split('-')[0]
				item['longitude'] = '-' + self.validate(store, 'location').split('-')[1]
				item['store_hours'] = ""
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = ""
				if item['store_number'] == "" or (item["store_number"] in self.uid_list):
				    return
				self.uid_list.append(item["store_number"])
				yield item

    def validate(self, store, attribute):
    	if attribute in store:
    		return store[attribute]
    	return ""


