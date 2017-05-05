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

class Petsupermarket(scrapy.Spider):
	name = "petsupermarket"
	uid_list = []
	domain = "https://www.petsupermarket.com/"

	def __init__(self):
		self.geolocator = Nominatim()

	def start_requests(self):
		request_url = "https://storemapper-herokuapp-com.global.ssl.fastly.net/api/users/2208/stores.js?callback=storeMapperCallback2"
		yield scrapy.Request(url=request_url, callback=self.parse_store)
	
	def parse_store(self, response):
		stores = json.loads(response.body[21:-1])['stores']
		for store in stores:
			item = ChainItem()

			item['store_number'] = store['id']
			item['store_name'] = store['name']
			item['address'] = store['address'];
			item['address2'] = ""
			item['phone_number'] = store['phone']
			item['latitude'] = store['latitude']
			item['longitude'] = store['longitude']

			location = self.geolocator.reverse("%s, %s" % (str(item['latitude']), str(item['longitude'])))

			try:
			    item['city'] = location.raw["address"]["city"]
			except:
			    if 'town' in location.raw["address"]:
			        item['city'] = location.raw["address"]["town"]

			item['state'] = location.raw["address"]["state"] if "state" in location.raw["address"] else ""
			item['zip_code'] = location.raw["address"]["postcode"]
			item['country'] = location.raw["address"]["country_code"].upper()
			if (item['country'] == ''):
				pdb.set_trace()
			item['other_fields'] = ""
			item['store_hours'] = ""
			item['coming_soon'] = 0

			yield item

	