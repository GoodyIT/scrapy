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

class Tacobueno(scrapy.Spider):
	name = "tacobueno"
	uid_list = []
	domain = "https://www.tacobueno.com/"

	def __init__(self):
		place_file = open('citiesusca.json', 'rb')
		self.place_reader = json.load(place_file)
		self.geolocator = ArcGIS()

	def start_requests(self):
		for city in self.place_reader:
			info = self.place_reader[city]
			if info['country'] == 'United States':
				request_url = "https://www.tacobueno.com/locations/&zip=" + info['zip_code']
				yield scrapy.Request(url=request_url, callback=self.parse_store)

	def parse_store(self, response):
		stores = response.xpath('//div[@tabindex="0"]')

		for store in stores:
			item = ChainItem()
			item['store_number'] = ''
			item['store_name'] = store.xpath('./h2/text()').extract_first()
			item['address'] = store.xpath(".//div[contains(@class, 'map-listing_item')]/address/text()").extract_first()
			if item['address'] == None:
				item['address'] = ''
			
			item['address2'] = ""
			item['phone_number'] = store.xpath(".//div[contains(@class, 'map-listing_item')]/ul/li[2]/a").extract_first()
			if item['phone_number'] == None:
				item['phone_number'] = ''
			item['city'] = store.xpath('.//@data-city').extract_first();
			item['country'] = "United States"
			item['latitude'] = ""
			item['longitude'] = ""
			gps = store.xpath('.//@data-gps').extract_first()
			if (gps != ""):
				item['latitude'] = gps.split(",")[0]
				item['longitude'] = gps.split(",")[1]
				location = self.geolocator.reverse("%s, %s" % (str(item['latitude']), str(item['longitude']))).raw
				item['state'] = location.get('Region', '')
			item['other_fields'] = ""
			hours = store.xpath(".//li[contains(@class, 'list-toggle-item')]/text()").extract()
			item['store_hours'] = ";".join(hours)
			item['coming_soon'] = 0
 
			yield item

	