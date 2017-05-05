import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class JohnstonmurphySpider(scrapy.Spider):
    name = "johnstonmurphy"
    uid_list = []

    headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
    start_urls = ['http://www.johnstonmurphy.com/store-locator']

    store_url = 'http://www.johnstonmurphy.com/on/demandware.store/Sites-johnston-murphy-us-Site/en_US/Stores-FindStores'
    
    def parse(self, response):
    	for country in response.xpath("//select[contains(@class, 'input-select country')]/option"):	    
				form_data = {
					'dwfrm_storelocator_address_country' : country.xpath("./@value").extract_first(),
					'dwfrm_storelocator_findbycountry' : 'Search'
				}

				request = FormRequest(url=self.store_url,
				              formdata=form_data,
				              headers=self.headers,
				              callback=self.parseStore)
				request.meta['country_name'] = country.xpath("./@label").extract_first()
				yield request
			
    def parseStore(self, response):
    	# try:
			stores = response.xpath('//td[contains(@class, "store-information")]')
			for store in stores:
				item = ChainItem()
				item['store_name'] = store.xpath('.//span[@class="header"]/text()').extract_first()
				item['store_number'] = ""
				item['address'] = store.xpath('.//div[@class="store-name"]/text()').extract()[1].strip()
				item['address2'] = ""
				item['phone_number'] = store.xpath('.//div[@class="store-name"]//text()').extract()[6]
				item['city'] = store.xpath('.//div[@class="store-name"]/text()').extract()[2].strip().split(",")[0].strip()
				item['state'] = self.getState(store.xpath('.//div[@class="store-name"]/text()').extract()[2].strip().split(",")[1].encode('utf-8').replace('\xc3\xb3n', '').replace('\xc3\xa9', 'e').split())
				item['zip_code'] = self.getZipCode(store.xpath('.//div[@class="store-name"]/text()').extract()[2].strip().split(",")[1].encode('utf-8').replace('\xc3\xb3n', '').replace('\xc3\xa9', 'e').split())
				item['country'] = response.meta['country_name']
				item['latitude'] = ""
				item['longitude'] = ""
				item['store_hours'] = ""
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = ""
				yield item

    def validate(self, store, attribute):
    	if attribute in store:
    		return store[attribute]
    	return ""

    def hasNumbers(self, str):
			return any(char.isdigit() for char in str)

    def getState(self, source):
    	state = ""
    	for item in source:
    		if self.hasNumbers(item):
    			return state.strip()
    		state += item + " "

    def getZipCode(self, source):
			zipcode = ""
			for item in source:
				if self.hasNumbers(item):
					i = source.index(item)
					while i < len(source):
						zipcode += source[i] + " "
						i += 1
					return zipcode.strip()    			
			return ""