import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb
from geopy.geocoders import Nominatim

class ElevenSpider(scrapy.Spider):
		name = "eleven"
		uid_list = []

		headers = { "Content-Type": "application/json", "Accept":"*/*" }

		def __init__(self):
			self.geolocator = Nominatim()
			place_file = open('all_code_list.csv', 'rb')
			self.place_reader = csv.reader(place_file)
			self.us_zip_code_list = []
			for row in self.place_reader:
				self.us_zip_code_list.append(row[0])

		def start_requests(self):
			request_url = "https://www.7-eleven.com/api/location/searchstores"
			form_data = {
				'Filters' : [],
				'PageNumber' : "0",
				"PageSize" : "100000",
				"SearchRangeMiles" : "1000000",
				"SourceLatitude" : "34.0522342",
				"SourceLongitude": "-118.2436849"
			}
			yield scrapy.Request(url=request_url, method="POST", body=json.dumps(form_data), headers=self.headers, callback=self.parse_store)

		# get longitude and latitude for a state by using google map.
		def parse_store(self, response):
			# try:
			stores = json.loads(response.body)
			for store in stores:
				item = ChainItem()
				item['store_name'] = self.validate(store, 'StoreName')
				item['store_number'] = self.validate(store, 'StoreNumber')
				item['address'] = self.validate(store, 'Address1') 
				item['address2'] = self.validate(store, 'Address2')
				item['phone_number'] = self.validate(store, 'Phone')
				item['city'] = self.validate(store, 'City')
				item['state'] = self.validate(store, 'State')
				item['zip_code'] = self.validate(store, 'Zip')
				item['latitude'] = self.validate(store, 'Latitude')
				item['longitude'] = self.validate(store,  'Longitude')
				item['store_hours'] = ""
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = ""
				if ( item['store_number'] != "" and item["store_number"] in self.uid_list):
				    return
				self.uid_list.append(item["store_number"])
				if (item['zip_code'].split('-')[0] in self.us_zip_code_list):
					item['country'] = "US"
					yield item

		def validate(self, store, attribute):
			if (attribute in store) and (store[attribute] != "null") :
				return store[attribute]
			return ""

		def get_info_from_latlng(self, lat, lng):
			location = self.geolocator.reverse("%s, %s" % (str(lat), str(lng)))
			try:
				return {
					'city': location.raw["address"]["town"] if "town" in location.raw["address"] else location.raw["address"]["city"],
					'state': location.raw["address"]["state"] if "state" in location.raw["address"] else "",
					'zip_code': location.raw["address"]["postcode"],
					'country': location.raw["address"]["country_code"].upper()
				}
			except:
				return {}
