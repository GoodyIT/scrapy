import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class Superstore(scrapy.Spider):
	name = "superstore"

	start_urls = ["https://www.realcanadiansuperstore.ca/store-locator/locations/all?showNonShoppable=true", ]
		
	def parse(self, response):
		store_list = json.loads(response.body)['searchResult']
		for store in store_list:
			item = ChainItem()
			item['store_number'] = store['details']['storeID']
			item['store_name'] = store['details']['storeName']
			item['address'] = store['details']['streetAddress']
			item['address2'] = ''
			item['phone_number'] = ''
			item['city'] = store['details']['city']
			item['state'] = store['details']['province']
			item['zip_code'] = store['details']['postalCode']
			item['country'] = "Canada"
			item['latitude'] = store['lat']
			item['longitude'] = store['lng']
			item['other_fields'] = ""
			item['store_hours'] = ""
			item['coming_soon'] = 0
 
			yield item


