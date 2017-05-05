import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class JambajuiceSpider(scrapy.Spider):
		name = "jambajuice"
		uid_list = []

		headers = { }

		def __init__(self):
			place_file = open('all_code_list.csv', 'rb')
			self.place_reader = csv.reader(place_file)

		def start_requests(self):
			for row in self.place_reader:
				request_url = "http://www.jambajuice.com/services/findastore.svc/GetStores?latitude=%s&longitude=%s" % (row[1], row[2])  
				yield scrapy.Request(url=request_url, callback=self.parse_store)

		# get longitude and latitude for a state by using google map.
		def parse_store(self, response):
			stores = json.loads(response.body)
			for store in stores:
				item = ChainItem()
				item['store_name'] = self.validate(store, 'StoreName')
				item['store_number'] = self.validate(store, 'StoreNumber')
				item['address'] = self.validate(store, 'StreetAddress1') 
				item['address2'] = self.validate(store, 'StreetAddress2')
				item['phone_number'] = self.validate(store, 'PhoneNumber').replace('.', '-')
				item['city'] = self.validate(store, 'City')
				item['state'] = self.validate(store, 'State')
				item['zip_code'] = self.validate(store, 'CityStatePostalCode')
				item['country'] = ""
				item['latitude'] = self.validate(store, 'Latitude')
				item['longitude'] = self.validate(store,  'Longitude')
				item['store_hours'] = "Weekday:" + self.validate(store,  'WeekdayHours') + ";" + "Friday:" + self.validate(store,  'FridayHours') + ";" + "Saturday:" + self.validate(store,  'SaturdayHours') + ";" + "Sunday:" + self.validate(store,  'SundayHours') + ";"
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
