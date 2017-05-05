import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class HardeesSpider(scrapy.Spider):
	name = "hardees"
	uid_list = []

	def __init__(self):
		place_file = open('cities_us.json', 'rb')
		self.place_reader = json.load(place_file)
		
	def start_requests(self):
		for info in self.place_reader:
			request_url = "http://maps.hardees.com/stores/search?country=&q=%s&brand_id=1&center_lat=%s&center_lng=%s&zoom=7" % (info['city'].replace(' ', '+'), info['latitude'], info['longitude'])

			yield scrapy.Request(url=request_url, callback=self.parse_store)

	def parse_store(self, response):
		body = response.xpath('//script[4]/text()').extract_first()
		stores = json.loads(body[body.find("map.markers = ") + 14:body.find("];") + 1])
		for store in stores:
			item = ChainItem()
			item['store_name'] = self.validate(store, 'title')
			item['store_number'] = self.validate(store, 'id')
			item['address'] = self.validate(self.validate(store, 'sidebar'), 'street')
			item['address2'] = ""
			item['phone_number'] = self.validate(self.validate(store, 'sidebar'), 'phone')
			item['city'] = self.validate(self.validate(store, 'sidebar'), 'city')
			item['state'] = self.validate(self.validate(store, 'sidebar'), 'state')
			item['zip_code'] = self.validate(self.validate(store, 'sidebar'), 'postal_code')
			item['country'] = "United States"
			item['latitude'] = self.validate(store, 'lat')
			item['longitude'] = self.validate(store, 'lng')
			item['store_hours'] = ""
			for hour in self.validate(self.validate(store, 'sidebar'), 'hours'):
				item['store_hours'] += hour['day'] + ":" + hour['time'] + ";"
			#item['store_type'] = info_json["@type"]
			item['other_fields'] = ""
			item['coming_soon'] = 0
			if item['store_number'] != "" and item['store_number'] in self.uid_list:
				continue
			self.uid_list.append(item['store_number'])
			yield item

	def validate(self, store, property):
		try:
			return store[property]
		except:
			return ""