import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

from lxml import html
from lxml.html import fromstring
from lxml import etree

class WhiteCastleSpider(scrapy.Spider):
	name = "whitecastle"
	uid_list = []
	used_states_list = []
	def __init__(self):
		place_file = open('cities_us.json', 'rb')
		self.states_list = json.load(place_file)

	def start_requests(self):
		for row in self.states_list:
			if row['state'] in self.used_states_list:
				continue 
			self.used_states_list.append(row['state'])
			count = 100
			for i in range(5):
				request_url = "https://www.whitecastle.com/api/location/search?form=%7B%22origin%22%3A%7B%22latitude%22%3A" + str(row['latitude']) + "%2C%22longitude%22%3A" + str(row['longitude']) + "%7D%2C%22count%22%3A" + str(count) + "%2C%22skip%22%3A" + str(i * count) + "%2C%22targets%22%3A%5B%22Castle%22%2C%22Retail%22%2C%22CraveMobile%22%5D%7D"
				yield scrapy.Request(url=request_url, callback=self.parseStore)
			break
	def parseStore(self, response):
		# try:
		stores = json.loads(response.body)
		for store in stores:
			item = ChainItem()
			item['store_name'] = self.validate(store, 'name')
			item['store_number'] = self.validate(store, 'id')
			item['address'] = self.validate(store, 'address') 
			item['address2'] = ""
			location_script = html.fromstring(self.validate(store, 'locationScript'))
			info = json.loads(location_script.xpath("//script/text()")[0])
			item['phone_number'] = self.validate(info, 'telephone')
			item['city'] = self.validate(store, 'city')
			item['state'] = self.validate(store, 'state')
			item['zip_code'] = self.validate(store, 'zip')
			item['country'] = "United States"
			item['latitude'] = self.validate(store, 'latitude')
			item['longitude'] = self.validate(store,  'longitude')
			item['store_hours'] = ";".join(self.validate(info, 'openingHours')) if len(self.validate(info, 'openingHours')) > 0 else ""
			#item['store_type'] = info_json["@type"]
			item['other_fields'] = ""
			item['coming_soon'] = 0
			if item['store_number'] != "" and item["store_number"] in self.uid_list:
				continue
			self.uid_list.append(item["store_number"])
			yield item

	def validate(self, store, attribute):
		if attribute in store:
			return store[attribute]
		return ""


