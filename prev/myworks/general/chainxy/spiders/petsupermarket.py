import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb
import usaddress

class Petsupermarket(scrapy.Spider):
	name = "petsupermarket"
	uid_list = []
	domain = "https://www.petsupermarket.com/"

	def __init__(self):
		place_file = open('citiesusca.json', 'rb')
		self.place_reader = json.load(place_file)

	def start_requests(self):
		request_url = "https://storemapper-herokuapp-com.global.ssl.fastly.net/api/users/2208/stores.js?callback=storeMapperCallback2"
		yield scrapy.Request(url=request_url, callback=self.parse_store)
	
	def parse_store(self, response):
		stores = json.loads(response.body[21:-1])['stores']
		for store in stores:
			item = ChainItem()

			item['store_number'] = store['name'].split('#')[1]
			item['store_name'] = store['name']
			item['phone_number'] = store['phone']
			item['latitude'] = store['latitude']
			item['longitude'] = store['longitude']
			addr = usaddress.parse(store['address'].replace('United States', ''))
			city = state = zip_code = street = ''
			for temp in addr:
				if temp[1] == 'PlaceName':
					city += temp[0].replace(',','') + ' '
				elif temp[1] == 'StateName':
					state = temp[0].replace(',','')
				elif temp[1] == 'ZipCode':
					zip_code = temp[0].replace(',','')
				else:
					street += temp[0].replace(',','') + ' '
			item['address'] = street
			item['city'] = city
			item['state'] =  state
			item['zip_code'] =  zip_code
			item['country'] = 'United States'
			item['address2'] = ''
			item['other_fields'] = ""
			item['store_hours'] = ""
			item['coming_soon'] = "0"
			if store['description'].find('Coming Soon!') != -1:
				item['coming_soon'] = "1"

			yield item

	