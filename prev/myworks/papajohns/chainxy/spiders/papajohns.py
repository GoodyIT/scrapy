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
		place_file = open('CA_PostalCode.json', 'rb')
		self.place_reader = json.load(place_file)

	def start_requests(self):
		for code in self.place_reader:
			request = scrapy.Request(url="https://www.papajohns.com/order/storesSearch?searchType=CARRYOUT&roomType=NON&zipcode=K0M1L0", callback=self.parse_store)
			request.meta['zip_code'] = code['code'];

			yield request

	def parse_store(self, response):
		stores = response.xpath('//article[@class="mapdata store-summary panel"]')
		for store in stores:
			pdb.set_trace()

			pdb.set_trace()
			item = ChainItem()
			item['store_number'] = store.xpath('.//div[@class="store-details"]/div/div[4]/div/text()').extract_first()
			item['store_name'] = ''
			item['address'] = store.xpath('.//h3/div[2]/p/text()').extract_first().split(',')[0]
			item['address2'] = ''
			item['phone_number'] = store.xpath('.//div[@class="store-details"]/div/div[1]/span[2]/a/text()').extract_first()
			item['city'] = store.xpath('.//h3/div[2]/p/text()').extract_first().split(',')[1].strip().split(' ')[0]
			item['state'] = store.xpath('.//h3/div[2]/p/text()').extract_first().split(',')[1].strip().split(' ')[1]
			item['zip_code'] = response.meta['zip_code']
			item['country'] = "Canada"
			item['latitude'] = store.xpath('//@data-maps-lat').extract_first()
			item['longitude'] = store.xpath('//@data-maps-long').extract_first()
			item['other_fields'] = ""

			hours = store.xpath('.//div[@class="store-details"]/div/div[@class="split-2"]/div/span/text()').extract_first()
			item['store_hours'] = hours
			if len(store.xpath('.//h3/div[2]/div[@class="store-directions"]/span/text()').extract_first()) > 0:
				item['coming_soon'] = 1
			else:
				item['coming_soon'] = 0
 
			yield item

	