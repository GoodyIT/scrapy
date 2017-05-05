import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class PotteryBarnKidsSpider(scrapy.Spider):
    name = "potterybarnkids"
    uid_list = []

    headers = { }

    def __init__(self):
        place_file = open('uscanplaces.csv', 'rb')
        self.place_reader = csv.reader(place_file)
    
    def start_requests(self): 	
        for row in self.place_reader:
          request_url = "http://www.potterybarnkids.com/search/stores.json?brands=PK&lat=%s&lng=%s&radius=25" % (row[0], row[1])  
          yield scrapy.Request(url=request_url, callback=self.parse_store)
    # get longitude and latitude for a state by using google map.
    def parse_store(self, response):
    	# try:
			stores = json.loads(response.body)["storeListResponse"]["stores"]
			for each_item in stores:
				store = each_item["properties"]
				item = ChainItem()
				item['store_name'] = self.validate(store, 'STORE_NAME')
				item['store_number'] = self.validate(store, 'STORE_NUMBER')
				item['address'] = self.validate(store, 'ADDRESS_LINE_1') 
				item['address2'] = self.validate(store, 'ADDRESS_LINE_2')
				item['phone_number'] = self.validate(store, 'PHONE_NUMBER_FORMATTED')
				item['city'] = self.validate(store, 'CITY')
				item['state'] = self.validate(store, 'STATE_PROVINCE')
				item['zip_code'] = self.validate(store, 'POSTAL_CODE')
				item['country'] = self.validate(store, 'COUNTRY_CODE')
				item['latitude'] = self.validate(store, 'LATITUDE')
				item['longitude'] = self.validate(store,  'LONGITUDE')
				item['store_hours'] = "SUN:" + self.validate(store,  'SUNDAY_HOURS_FORMATTED') + ";" + "MON:" + self.validate(store,  'MONDAY_HOURS_FORMATTED') + ";" + "TUE:" + self.validate(store,  'TUESDAY_HOURS_FORMATTED') + ";" + "WED:" + self.validate(store,  'WEDNESDAY_HOURS_FORMATTED') + ";" + "THU:" + self.validate(store,  'THURSDAY_HOURS_FORMATTED') + ";" + "FRI:" + self.validate(store,  'FRIDAY_HOURS_FORMATTED') + ";" + "SAT:" + self.validate(store,  'SATURDAY_HOURS_FORMATTED') + ";"  
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


