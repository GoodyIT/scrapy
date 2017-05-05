import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class FireHouseSubsSpider(scrapy.Spider):
    name = "firehousesubs"
    uid_list = []

    headers = { }

    def __init__(self):
        place_file = open('uscanplaces.csv', 'rb')
        self.place_reader = csv.reader(place_file)
    
    def start_requests(self):
        for row in self.place_reader:
            request_url = "https://www.firehousesubs.com/Locations/GetNearbyLocations/?latitude=%s&longitude=%s" % (row[0], row[1])  
            yield scrapy.Request(url=request_url, callback=self.parse_store)

    # get longitude and latitude for a state by using google map.
    def parse_store(self, response):
    	# try:
			stores = json.loads(response.body)
			for store in stores:
				item = ChainItem()
				pdb.set_trace()
				item['store_name'] = self.validate(store, 'siteId')
				item['store_number'] = self.validate(store, 'title')
				item['address'] = self.validate(store, 'address') 
				item['address2'] = self.validate(store, 'address2')
				item['phone_number'] = self.validate(store, 'phone')
				item['city'] = self.validate(store, 'city')
				item['state'] = self.validate(store, 'state')
				item['zip_code'] = self.validate(store, 'zip')
				item['country'] = ""
				item['latitude'] = self.validate(store, 'latitude')
				item['longitude'] = self.validate(store,  'longitude')
				item['store_hours'] = self.validate(store,  'hoursOpen')
				#item['store_type'] = info_json["@type"]
				item['other_fields'] = ""
				item['coming_soon'] = self.validate(store,  'isComingSoon')
				if item['store_number'] == "" or (item["store_number"] in self.uid_list):
				    return
				self.uid_list.append(item["store_number"])
				yield item

    def validate(self, store, attribute):
    	if attribute in store:
    		return store[attribute]
    	return ""


