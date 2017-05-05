import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class ChurchslocatorSpider(scrapy.Spider):
		name = "churchslocator"
		uid_list = []

		headers = { }

		def __init__(self):
			place_file = open('all_code_list.csv', 'rb')
			self.place_reader = csv.reader(place_file)

		def start_requests(self):
			request_url = "http://churchslocator.nextxnow.com/controller/locator/getIntlStores"
			yield scrapy.Request(url=request_url, callback=self.parse_international_store)
			request_url = "http://churchslocator.nextxnow.com/controller/locator/getLocations?lat=41.2523634&lng=-95.99798829999997&keyword=&start=0&limit=100000"
			yield scrapy.Request(url=request_url, callback=self.parse_store)

		def parse_store(self, response):
			stores = json.loads(response.body)['data']
			for store in stores:
				item = ChainItem()
				item['store_name'] = self.validate(store, 'accountName')
				item['store_number'] = self.validate(store, 'accountNumber')
				item['address'] = self.validate(store, 'address') 
				item['address2'] = ""
				item['phone_number'] = self.validate(store, 'phone')
				item['city'] = self.validate(store, 'city')
				item['state'] = self.validate(store, 'state')
				item['zip_code'] = self.validate(store, 'zip')
				item['country'] = self.validate(store, 'country')
				item['latitude'] = self.validate(store, 'lat')
				item['longitude'] = self.validate(store,  'lng')
				item['store_hours'] = ""
				if self.validate(store, 'hoursets') != "":
					hour_list = json.loads(self.validate(store, 'hoursets'))[0]['hours']
					for hour in hour_list:
						item['store_hours'] += hour['Day'] + ":" + hour['Start'] + "-" + hour['End'] + ";"
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = ""
				if item['store_number'] == "" or (item["store_number"] in self.uid_list):
				    return
				self.uid_list.append(item["store_number"])
				yield item

		def parse_international_store(self, response):
			stores = json.loads(response.body)['extra']['detail']
			for store in stores:
				item = ChainItem()
				item['store_name'] = ""
				item['store_number'] = ""
				item['address'] = self.validate(store, 'address') 
				item['address2'] = ""
				item['phone_number'] = ""
				item['city'] = self.validate(store, 'city')
				item['state'] = ""
				item['zip_code'] = ""
				item['country'] = self.validate(store, 'country')
				item['latitude'] = ""
				item['longitude'] = ""
				item['store_hours'] = ""
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = ""
				if item['address'] != "":
					yield item

		def validate(self, store, attribute):
			if attribute in store:
				return store[attribute]
			return ""
