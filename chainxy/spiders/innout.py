import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class InnoutSpider(scrapy.Spider):
    name = "innout"
    uid_list = []

    headers = { "X-Requested-With": "XMLHttpRequest", "Accept":"*/*" }

    def __init__(self):
        place_file = open('uscanplaces.csv', 'rb')
        self.place_reader = csv.reader(place_file)
    
    def start_requests(self):
        for row in self.place_reader:
            request_url = "http://locations.in-n-out.com/api/finder/search/?showunopened=false&latitude=%s&longitude=%s&maxdistance=175&maxresults=25" % (row[0], row[1])  
            yield scrapy.Request(url=request_url, headers=self.headers, callback=self.parse_store)

    # get longitude and latitude for a state by using google map.
    def parse_store(self, response):
    	# try:
			stores = json.loads(response.body)
			for store in stores:
				item = ChainItem()
				item['store_name'] = self.validate(store, 'Name')
				item['store_number'] = self.validate(store, 'StoreNumber')
				item['address'] = self.validate(store, 'StreetAddress') 
				item['address2'] = self.validate(store, 'Address2')
				item['phone_number'] = ""
				item['city'] = self.validate(store, 'City')
				item['state'] = self.validate(store, 'State')
				item['zip_code'] = self.validate(store, 'ZipCode')
				item['country'] = ""
				item['latitude'] = self.validate(store, 'Latitude')
				item['longitude'] = self.validate(store,  'Longitude')
				item['store_hours'] = ""
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


