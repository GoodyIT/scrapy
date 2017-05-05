import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

from lxml import html
from lxml.html import fromstring

class MauricesSpider(scrapy.Spider):
		name = "maurices"
		uid_list = []

		headers = { }

		def __init__(self):
			place_file = open('all_code_list.csv', 'rb')
			self.place_reader = csv.reader(place_file)
			self.us_zip_code_list = []
			for row in self.place_reader:
				self.us_zip_code_list.append(row[0])

		def start_requests(self):
			request_url = "http://maps.maurices.com/api/getAsyncLocations?template=search&level=search&radius=1000000&search=Toronto+OH%2C+United+States&_=1493019550740"
			yield scrapy.Request(url=request_url, callback=self.parse_store)

		# get longitude and latitude for a state by using google map.
		def parse_store(self, response):
			stores = json.loads(response.body)["markers"]
			for store in stores:
				try:
					item = ChainItem()
					item['latitude'] = self.validate(store, 'lat')
					item['longitude'] = self.validate(store, 'lng')
					info = html.fromstring(store['info'])
					item['store_name'] = self.validate_xpath(info.xpath("//div[@class='location-name']/text()"))
					item['store_number'] = ""
					item['address'] = self.validate_xpath(info.xpath("//p[@class='address']/span/text()"))
					item['address2'] = ""
					item['phone_number'] = info.xpath("//a[@class='phone']/text()")[1].strip()
					item['city'] = info.xpath("//p[@class='address']/span/text()")[-1].split(',')[0].strip()
					item['state'] = info.xpath("//p[@class='address']/span/text()")[-1].split(',')[1].split()[0].strip()
					item['zip_code'] = info.xpath("//p[@class='address']/span/text()")[-1].split(',')[1].split()[1].strip()
					item['country'] = ""
					if (item['zip_code'].split('-')[0] in self.us_zip_code_list):
						item['country'] = "US"
					else:
						item['country'] = "CA"				
					item['store_hours'] = ""
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = ""
					yield item
				except:
					continue

		def validate(self, store, attribute):
			if attribute in store:
				return store[attribute]
			return ""

		def validate_xpath(self, xpath_obj):
			try:
				return xpath_obj[0].strip()
			except:
				return ""