import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class SephoraSpider(scrapy.Spider):
		name = "sephora"
		uid_list = []
		start_request = "http://www.sephora.com/storelist"
		headers = { "Content-Type": "application/json", "Accept":"*/*" }

		def __init__(self):
			place_file = open('all_code_list.csv', 'rb')
			self.place_reader = csv.reader(place_file)
			self.us_zip_code_list = []
			for row in self.place_reader:
				self.us_zip_code_list.append(row[0])

		def start_requests(self):
			yield scrapy.Request(url=self.start_request, callback=self.parse_stores_list)

		def parse_stores_list(self, response):
			for group in response.xpath("//ul[contains(@class, 'u-listReset')]"):
				for store in group.xpath("./li"):
					yield scrapy.Request(url=store.xpath("./a/@href").extract_first(), callback=self.parse_store)

    # get longitude and latitude for a state by using google map.
		def parse_store(self, store):
			# try:
				item = ChainItem()
				item['store_name'] = self.validate(store.xpath('//*[@id="main"]/div/h1/text()'))
				item['store_number'] = ""
				item['address'] = self.validate(store.xpath('//li[@class="store-address1"]/text()'))
				item['address2'] = ""
				item['city'] = self.replaceWithNone(self.validate(store.xpath('//li[@class="store-address2"]/text()')).split(",")[0])
				item['state'] = self.validate(store.xpath('//li[@class="store-address2"]/text()')).split(",")[1].split()[0]
				item['zip_code'] = self.validate(store.xpath('//li[@class="store-address2"]/text()')).split(",")[1].split()[1]
				item["country"] = ""
				if (item['zip_code'].split('-')[0] in self.us_zip_code_list):
					item['country'] = "US"
				else:
					item['country'] = "CA"				
				item['phone_number'] = self.validate(store.xpath('//li[@class="phone"]/text()')).split(":")[1].strip()
				item['latitude'] = ""
				item['longitude'] = ""
				_hour_list = store.xpath('//ul[@class="u-listReset"]')[1]
				hour_list = _hour_list.xpath('./li/text()').extract()
				del hour_list[0]
				item['store_hours'] = ""
				for hour in hour_list:
					item['store_hours'] += self.replaceWithNone(hour) + ";"
				# item['store_type'] = info_json["@type"]
				item['store_hours'] = item["store_hours"].encode("utf-8").replace('\xc2\xa0', '')
				item['other_fields'] = ""
				item['coming_soon'] = ""
				if item['store_name'] == "" or (item["store_name"] in self.uid_list):
				    return
				self.uid_list.append(item["store_name"])					
				yield item

		def validate(self, xpath_obj):
			try:
				return xpath_obj.extract_first().replace('\n','').replace('\r','').strip()
			except:
				return ""

		def replaceWithNone(self, str):
			try:
				return str.encode('utf-8').replace('\r', '').replace('\n','').replace('\t','').replace('\xc2\xa0', '').strip()
			except:
				return ""
		def replaceWithBlank(self, str):
			try:
				return str.replace('\r', ' ').replace('\n',' ').replace('\t',' ').replace(',', ' ')
			except:
				return ""			