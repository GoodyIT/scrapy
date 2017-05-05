import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class DollaramaSpider(scrapy.Spider):
	name = "dollarama"
	uid_list = []

	def __init__(self):
		place_file = open('citiesusca.json', 'rb')
		self.place_reader = json.load(place_file)

	def start_requests(self):
		for city in self.place_reader:
			info = self.place_reader[city]
			if info['country'] == 'Canada':
				request_url = "http://www.dollarama.com/wp-content/plugins/store-locator/sl-xml.php?mode=gen&lat=%s&lng=%s&radius=500" % (info['latitude'], info['longitude'])
				yield scrapy.Request(url=request_url, callback=self.parse_store)

	def parse_store(self, response):
		stores = response.xpath('//marker')
		for store in stores:
			item = ChainItem()
			item['store_name'] = self.validate(store.xpath('./@name'))
			item['store_number'] = ""
			item['address'] = self.validate(store.xpath('./@street'))
			item['address2'] = ""
			item['phone_number'] = self.validate(store.xpath('./@phone'))
			item['city'] = self.validate(store.xpath('./@city'))
			item['state'] = self.validate(store.xpath('./@state'))
			item['zip_code'] = self.validate(store.xpath('./@zip'))
			item['country'] = "Canada"
			item['latitude'] = self.validate(store.xpath('./@lat'))
			item['longitude'] = self.validate(store.xpath('./@lng'))
			item['store_hours'] = self.validate(store.xpath('./@lng')).replace('||', ';')
			#item['store_type'] = info_json["@type"]
			item['other_fields'] = ""
			item['coming_soon'] = 0
			if item['store_name'] != "" and item['store_name'] in self.uid_list:
				continue
			self.uid_list.append(item['store_name'])
			yield item

	def validate(self, xpath_obj):
		try:
			return xpath_obj.extract_first().strip().encode('utf8').replace('\xc3\xb4', 'o').replace("&#39", "'").replace('&amp;nbsp;', '').replace('&nbsp;', '')
		except:
			return ""