import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class JourneysSpider(scrapy.Spider):
		name = "journeys"
		uid_list = []

		headers = { }

		def start_requests(self):
			request_url = "https://www.journeys.com/stores_all"  
			yield scrapy.Request(url=request_url, callback=self.parse_store)

    # get longitude and latitude for a state by using google map.
		def parse_store(self, response):
			# try:
			try:
				stores = response.xpath("//address[@class='address-store']")
				for store in stores:
					item = ChainItem()
					item['store_name'] = self.replaceWithNone(store.xpath("./strong/a/text()").extract()[0])
					item['store_number'] = self.replaceWithNone(store.xpath("./strong/a/text()").extract()[1])
					item['address'] = self.replaceWithNone(store.xpath('./text()').extract()[1]) 
					item['address2'] = ""
					item['phone_number'] = self.replaceWithNone(store.xpath('./text()').extract()[3])
					item['city'] = store.xpath('./text()').extract()[2].split(',')[0].replace('\r','').replace('\n','').strip()
					item['state'] = store.xpath('./text()').extract()[2].split(',')[1].replace('\r','').replace('\n','').strip().split()[0]
					item['zip_code'] = store.xpath('./text()').extract()[2].split(',')[1].replace('\r','').replace('\n','').strip().split()[1]
					item['country'] = ""
					item['latitude'] = ""
					item['longitude'] = ""
					item['store_hours'] = ""
					# item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = ""
					if item['store_number'] == "" or (item["store_number"] in self.uid_list):
					    return
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
				return str.replace('\r', '').replace('\n','').replace('\t','').strip()
			except:
				return ""
		def replaceWithBlank(self, str):
			try:
				return str.replace('\r', ' ').replace('\n',' ').replace('\t',' ').replace(',', ' ').strip()
			except:
				return ""			