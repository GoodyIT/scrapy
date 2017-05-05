import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class Papajohns(scrapy.Spider):
	name = "papajohns"
	uid_list = []
	domain = "https://www.papajohns.com/"

	def __init__(self):
		place_file = open('citiesusca.json', 'rb')
		self.place_reader = json.load(place_file)

	def start_requests(self):
		# for city in self.place_reader:
		# 	info = self.place_reader[city]
		# 	if info['country'] == 'Canada':
		# 		request_url = "https://www.papajohns.com/order/storesSearch?latitude=%s&longitude=%s&searchType=CARRYOUT" % (info['latitude'], info['longitude'])
		# 		request = scrapy.Request(url=request_url, callback=self.parse_store)
		# 		request.meta['city'] = info['city']
		# 		request.meta['state'] = info['state']
		# 		request.meta['zip_code'] = info['zip_code']
		# 		request.meta['lat'] = info['latitude']
		# 		request.meta['lng'] = info['longitude']
		# 		yield request;
		yield scrapy.Request(url="https://www.papajohns.com/order/storesSearch?searchType=CARRYOUT&roomType=NON&latitude=-123.0386&longitude=49.1853", callback=self.parse_store)

	def parse_store(self, response):
		# pdb.set_trace()
		stores = response.xpath('//article[@class="mapdata store-summary panel active-panel"]')
		for store in stores:
			pdb.set_trace()
			item = ChainItem()
			item['store_number'] = store.xpath('.//div[@class="store-details"]/div/div[4]/div/text()').extract_first()
			item['store_name'] = store.xpath('.//span[@class="store-location-label"]/text()').extract()[1].strip()
			item['address'] = store.xpath('.//h3/div[2]/p/text()').extract_first()
			item['address2'] = ''
			item['phone_number'] = store.xpath('.//div[@class="store-details"]/div/div[1]/span[2]/a/text()').extract_first()
			item['city'] = response.meta['city']
			item['state'] = response.meta['state']
			item['zip_code'] = response.meta['zip_code']
			item['country'] = "Canada"
			item['latitude'] = response.meta['lat']
			item['longitude'] = response.meta['lng']
			item['other_fields'] = ""

			hours = store.xpath('.//div[@class="store-details"]/div/div[@class="split-2"]/div/span/text()').extract()[1]
			# item['store_hours'] = ";".join(hours)
			item['store_hours'] = hours
			item['coming_soon'] = 0
 
			yield item

	