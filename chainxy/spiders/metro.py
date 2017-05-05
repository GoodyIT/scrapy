import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class MetroSpider(scrapy.Spider):
		name = "metro"
		uid_list = []
		domain = "https://www.metro.ca"

		def start_requests(self):
			request_url = "https://www.metro.ca/en/find-a-grocery"
			form_data = {
				'postalCode' : '',
				'provinceCode': 'ON',
				'city': 'London'
			}
			yield FormRequest(url=request_url, formdata=form_data, callback=self.parseUrl)

		def parseUrl(self, response):
			for url in response.xpath('//a[@class="fs--grocery-detail"]/@href').extract():
				item = ChainItem()
				item['store_number'] = url.split('/')[-1]
				request = scrapy.Request(url=self.domain+url, callback=self.parseStore)
				request.meta['item'] = item
				yield request

		def parseStore(self, response):
			item = response.meta['item']
			item['store_name'] = self.validate(response.xpath('//p[@class="sd--name"]/text()'))
			item['address'] = response.xpath('//div[@class="sd--content"]/p[2]/text()').extract()[0].strip().replace(' ', '').replace('\n', ' ')
			item['address2'] = ""
			item['phone_number'] = response.xpath('//div[@class="telephone"]/div[1]/text()[2]').extract_first().strip()
			item['city'] = response.xpath('//div[@class="sd--content"]/p[2]/text()').extract()[1].strip().split(',')[0].strip()
			item['state'] = response.xpath('//div[@class="sd--content"]/p[2]/text()').extract()[1].strip().split(',')[1].strip()
			item['zip_code'] = response.xpath('//div[@class="sd--content"]/p[2]/text()').extract()[2].strip()
			pdb.set_trace()
			item['country'] = "Canada"
			item['latitude'] = response.xpath('//div[@class="map-canvas"]/@data-store-lat').extract_first()
			item['longitude'] = response.xpath('//div[@class="map-canvas"]/@data-store-lng').extract_first()
			item['store_hours'] = ""
			for day in self.validate(store, "regularHours"):
				item['store_hours'] += day['day'] + ":" + day['openTime'] + "-" + day['closeTime'] + ";"
			#item['store_type'] = info_json["@type"]
			item['other_fields'] = ""
			item['coming_soon'] = 0
			yield item

		def validate(self, xpath):
			try:
				return xpath.extract_first().strip()
			except:
				return ""