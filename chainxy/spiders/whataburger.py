import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class WhataBurgerSpider(scrapy.Spider):
	name = "whataburger"
	uid_list = []

	headers = {}

	def __init__(self):
	  place_file = open('cities.json', 'rb')
	  self.place_reader = json.load(place_file)

	def start_requests(self):
	  for row in self.place_reader:
			city = '+'.join(row['city'].split(' '))
			request_url = "https://locations.whataburger.com/search.html?q=%s" % city
			yield scrapy.Request(url=request_url, callback=self.parse_store)

	# get longitude and latitude for a state by using google map.
	def parse_store(self, response):
		try:
			stores = response.xpath('//div[@class=$val]', val="location")
			for store in stores:
				item = ChainItem()
				item['store_name'] = self.validate(store.xpath('.//a[@class="location-title-link"]/span/text()'))
				item['store_number'] = self.validate(store.xpath('@id'))
				item['address'] = self.validate(store.xpath('.//span[@class="c-address-street c-address-street-1"]/text()')) 
				item['address2'] = ""
				item['phone_number'] = ""
				item['city'] = self.validate(store.xpath('.//span[@class="c-address-city"]/span/text()'))
				item['state'] = self.validate(store.xpath('.//abbr[@class="c-address-state"]/text()'))
				item['zip_code'] = self.validate(store.xpath('.//span[@class="c-address-postal-code"]/text()'))
				item['country'] = self.validate(store.xpath('.//abbr[@class="c-address-country-name c-address-country-us"]/text()'))
				item['latitude'] = ""
				item['longitude'] = ""
				item['store_hours'] = ""
				# item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = ""
				if item['store_number'] == "" or (item["store_number"] in self.uid_list):
				    return
				self.uid_list.append(item["store_number"])
				yield item
		except:
			pass
	def validate(self, xpath_obj):
		try:
			return xpath_obj.extract_first().strip()
		except:
			return ""


