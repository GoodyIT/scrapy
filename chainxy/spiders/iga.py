import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class IgaSpider(scrapy.Spider):
		name = "iga"
		uid_list = []

		def start_requests(self):
			for page in range(220):
				request_url = "https://www.iga.com/consumer/locator.aspx?SearchText=61911&pg=%s" % page
				yield scrapy.Request(url=request_url, callback=self.parseStore)

		def parseStore(self, response):
			# try:
			stores = response.xpath('//ol[@class="vlist results"]/li')
			for store in stores:
				item = ChainItem()
				# pdb.set_trace()
				item['store_name'] = self.validate(store.xpath('.//div[@class="fn org"]/text()')).split('.')[1].strip()
				item['store_number'] = ""
				item['address'] = self.validate(store.xpath('.//div[@class="street-address"]/text()'))
				item['address2'] = ""
				item['phone_number'] = store.xpath('.//span[@class="tel"]/text()').extract_first().split()[0] + store.xpath('.//span[@class="tel"]/text()').extract_first().split()[1]
				item['city'] = self.validate(store.xpath('.//span[@class="locality"]/text()')).split(',')[0]
				item['state'] = self.validate(store.xpath('.//span[@class="region"]/text()'))
				item['zip_code'] = self.validate(store.xpath('.//span[@class="postal-code"]/text()'))
				item['country'] = "United States"
				item['latitude'] = store.xpath('.//a[contains(@id,"hlDirections")]/@href').extract_first().split('=')[1].split(',')[0]
				item['longitude'] = store.xpath('.//a[contains(@id,"hlDirections")]/@href').extract_first().split('=')[1].split(',')[1] 
				item['store_hours'] = ""
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = 0
				yield item

		def validate(self, xpath_obj):
			try:
				return xpath_obj.extract_first().strip()
			except:
				return ""