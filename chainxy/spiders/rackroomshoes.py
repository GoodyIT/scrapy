import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class RackRoomShoesSpider(scrapy.Spider):
		name = "rackroomshoes"
		uid_list = []

		def start_requests(self):
			request_url = "https://www.rackroomshoes.com/deichmannws/storelocator/zip/19971/10000?_=1493345725575"
			yield scrapy.Request(url=request_url, callback=self.parseStore)

		def parseStore(self, response):
			# try:
			stores = json.loads(response.body)
			for store in stores:
				item = ChainItem()
				item['store_name'] = ""
				item['store_number'] = self.validate(store, "storeId")
				item['address'] = self.validate(self.validate(store, "address"), "street1").strip()
				item['address2'] = self.validate(self.validate(store, "address"), "street2").strip()
				item['phone_number'] = self.validate(store, "phone").replace('.', '-')
				item['city'] = self.validate(self.validate(store, "address"), "city")
				item['state'] = self.validate(self.validate(store, "address"), "state")
				item['zip_code'] = self.validate(self.validate(store, "address"), "zipCode")
				item['country'] = "United States"
				item['latitude'] = self.validate(self.validate(store, "geoPoint"), "latitude")
				item['longitude'] = self.validate(self.validate(store, "geoPoint"), "longitude")
				item['store_hours'] = ""
				for day in self.validate(store, "regularHours"):
					item['store_hours'] += day['day'] + ":" + day['openTime'] + "-" + day['closeTime'] + ";"
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = 0
				yield item

		def validate(self, store, property):
			if property in store:
				return store[property]
			return ""