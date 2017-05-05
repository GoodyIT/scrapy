import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class SwarovskiSpider(scrapy.Spider):
    name = "swarovski"
    uid_list = []

    headers = { }
    
    def start_requests(self):
			request_url = "http://www.swarovski.com/is-bin/INTERSHOP.enfinity/WFS/SCO-Web_AA-Site/en_US/-/EUR/SPAG_Storefinder-GetStoresJSON?lat=34.0522342&lng=-118.2436849&radius=1000000"
			yield scrapy.Request(url=request_url, callback=self.parse_store)

    # get longitude and latitude for a state by using google map.
    def parse_store(self, response):
    	# try:
			stores = json.loads(response.body)["stores"]
			for store in stores:
				item = ChainItem()
				item['store_name'] = self.validate(store, 'name')
				item['store_number'] = self.validate(store, 'storeid')
				item['address'] = self.validate(store, 'address') 
				item['address2'] = self.validate(store, 'address2')
				item['phone_number'] = self.validate(store, 'phone')
				item['city'] = self.validate(store, 'place')
				item['state'] = self.validate(store, 'region')
				item['zip_code'] = self.validate(store, 'zip')
				item['country'] = self.validate(store, 'country')
				item['latitude'] = self.validate(store, 'coordinates')["lat"]
				item['longitude'] = self.validate(store, 'coordinates')["lng"]
				item['store_hours'] = ""
				hours = self.validate(store, 'businessHoursStructured')
				for hour in hours:
					if hour['from_m'] != "":
						item['store_hours'] += hour['day_of_week_char'] + ":" + hour['from_m'] + "-" + hour['to_m'] + ";"
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = ""
				if item['store_number'] == "" or (item["store_number"] in self.uid_list):
				    return
				self.uid_list.append(item["store_number"])
				yield item

    def validate(self, store, attribute):
    	if attribute in store:
    		return store[attribute]
    	return ""


