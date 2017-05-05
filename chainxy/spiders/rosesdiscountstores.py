import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb
from geopy.geocoders import ArcGIS

class Rosesdiscountstores(scrapy.Spider):
	name = "rosesdiscountstores"
	uid_list = []
	domain = "https://www.rosesdiscountstores.com/"

	def __init__(self):
		place_file = open('states.json', 'rb')
		self.place_reader = json.load(place_file)
		self.geolocator = ArcGIS()

	def start_requests(self):
		for state in self.place_reader:
			request_url = "http://www.rosesdiscountstores.com/store/searchourstorelocations"
			formdata = {'locale':'en','from':state['code'],'distance':'250'}
			request = FormRequest(url=request_url,
				              formdata=formdata,
				              callback=self.parse_store)
			request.meta['state'] = state['name']
			request.meta['lat'] = state['latitude']
			request.meta['lng'] = state['longitude']

			yield request

	def parse_store(self, response):
		stores = response.xpath('//div[@class="VWStoreInfo"]')

		for store in stores:
			item = ChainItem()
			item['store_name'] = store.xpath('.//h3/text()').extract_first()
			if item['store_name'] == None:
				continue

			item['store_number'] = ''
			address = store.xpath(".//p/text()").extract_first().split(',')
			item['address'] = address[0]
			for idx, value in enumerate(address):
			    if idx == len(address) - 1:
		        	item['phone_number'] = value

			if item['phone_number'] in self.uid_list:
				continue
			else:
				self.uid_list.append(item['phone_number'])

			item['address2'] = ""
			item['city'] = address[1].strip()
			item['state'] = response.meta['state']
			item['country'] = "United States"
			item['latitude'] = response.meta['lat']
			item['longitude'] = response.meta['lng']
			item['other_fields'] = ""

			hours = store.xpath(".//p[2]/text()").extract()
			item['store_hours'] = ";".join(hours)
			item['coming_soon'] = 0
 
			yield item

	