import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb
import re

class TractorSupplySpider(scrapy.Spider):
	name = "tractorsupply"
	uid_list = []

	headers = {}

	def __init__(self):
	  place_file = open('citiesusca.json', 'rb')
	  self.place_reader = json.load(place_file)

	def start_requests(self):
		for row in self.place_reader:
			info = self.place_reader[row]
			request_url = "https://www.tractorsupply.com/tsc/store-locator?city=%s&state=%s&zipCode=" % (info['city'].replace(' ', '+'), info['state'])
			yield scrapy.Request(url=request_url, callback=self.parse_store)

	# get longitude and latitude for a state by using google map.
	def parse_store(self, response):
		try:
			stores = response.xpath('//div[contains(@class, "cl-list")]//form')
			for each_item in stores:
				item = ChainItem()
				re_store = each_item.xpath('./script/text()').extract_first().encode('utf-8').strip()
				store = each_item.xpath('./div[contains(@class, "storelocator_searchresults")]')[0]
				item['store_name'] = ""
				item['store_number'] = self.validate_re(re.search(r'physicalStoreId":(.*?),\n', re_store).group(1))
				item['address'] = self.validate(store.xpath('.//span[@class="address_sl_sr"]/text()')) 
				item['address2'] = ""
				item['phone_number'] = self.validate(store.xpath('.//span[@class="telephone_sl_sr"]/text()'))

				item['city'] = self.replaceWithNone(store.xpath('.//span[@class="cityzip_sl_sr"]/text()').extract_first()).split(',')[0].strip()
				item['state'] = self.replaceWithNone(store.xpath('.//span[@class="cityzip_sl_sr"]/text()').extract_first()).split(',')[1].split()[0]
				item['zip_code'] = self.replaceWithNone(store.xpath('.//span[@class="cityzip_sl_sr"]/text()').extract_first()).split(',')[1].split()[1]
				item['country'] = 'United States'
				item['latitude'] = self.validate_re(re.search(r'latitude":(.*?),\n', re_store).group(1))
				item['longitude'] = self.validate_re(re.search(r'longitude":(.*?),\n', re_store).group(1))
				item['store_hours'] = self.validate_re(re.search(r'storeHours":(.*?),\n', re_store).group(1)).replace('|',';')
				# item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = ""
				if item['store_number'] != "" and item["store_number"] in self.uid_list:
				    continue
				self.uid_list.append(item["store_number"])
				yield item
		except:
			pass
	def validate(self, xpath_obj):
		try:
			return xpath_obj.extract_first().strip()
		except:
			return ""

	def replaceWithNone(self, str):
		try:
			return str.encode('utf-8').replace('\r', '').replace('\n','').replace('\t','').replace('\xc2\xa0', ' ').strip()
		except:
			return ""

	def validate_re(self, str):
		try:
			return str.replace("'", "")
		except:
			""