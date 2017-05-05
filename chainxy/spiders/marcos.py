import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class MarcosSpider(scrapy.Spider):
    name = "marcos"
    uid_list = []

    headers = { }
    
    def start_requests(self):
			request_url = "https://www.marcos.com/data/locations"
			yield scrapy.Request(url=request_url, callback=self.parse_store)

    # get longitude and latitude for a state by using google map.
    def parse_store(self, response):
    	# try:
			stores = json.loads(response.body)["items"]
			for store in stores:
				try:
					item = ChainItem()
					item['store_name'] = self.validate(store, 'name')
					item['store_number'] = self.validate(store, 'chain_id')
					item['address'] = self.validate(store, 'address1') 
					item['address2'] = ""
					item['phone_number'] = self.validate(store, 'phone')
					item['city'] = self.validate(store, 'city')
					item['state'] = self.validate(store, 'state')
					item['zip_code'] = self.validate(store, 'zip')
					item['country'] = self.validate(store, 'country')
					item['latitude'] = self.validate(store, 'manual_latitude')
					item['longitude'] = self.validate(store, 'manual_longitude')
					item['store_hours'] = ""
					if 'hoursets' in store:
						hours = self.validate(store, 'hoursets')[0]['hours']
						for hour in hours:
							item['store_hours'] += hour + ":" + hours[hour] + ";"
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = self.validate(store, 'status')
					if item['store_number'] != "" and item["store_number"] in self.uid_list:
					    return
					self.uid_list.append(item["store_number"])
					yield item
				except:
					pdb.set_trace()
					pass

    def validate(self, store, attribute):
    	if attribute in store:
    		return store[attribute]
    	return ""


