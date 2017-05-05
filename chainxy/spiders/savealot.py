import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem

class SaveALotSpider(scrapy.Spider):
    name = "savealot"
    uid_list = []

    def __init__(self):
        place_file = open('uscanplaces.csv', 'rb')
        self.place_reader = csv.reader(place_file)
    
    def start_requests(self):
        index = 1
        for row in self.place_reader:
            request_url = "https://locator-api.localsearchprofiles.com/api/LocationSearchResults/?configuration=ddc821e6-0b30-458f-b427-91311fc99860&&searchby=address&address=%s,%s" % (row[0], row[1])  
            yield scrapy.Request(url=request_url, callback=self.parse_store)

    # get longitude and latitude for a state by using google map.
    def parse_store(self, response):
    	# try:
				stores = json.loads(response.body)["Hit"]
        
				for each_item in stores:
					item = ChainItem()
					store = each_item['Fields']
					item['store_name'] = self.validate(store, 'LocationName')
					item['store_number'] = self.validate(store, 'StoreNumber')
					item['address'] = self.validate(store, 'Address1') 
					item['address2'] = self.validate(store, 'Address2')
					item['phone_number'] = self.validate(store, 'PhoneDisplay')
					item['city'] = self.validate(store, 'City')
					item['state'] = self.validate(store, 'State')
					item['zip_code'] = self.validate(store, 'Zip')
					item['country'] = 'US'
					item['latitude'] = self.validate(store, 'Latlng').split(',')[0]
					item['longitude'] = self.validate(store,  'Latlng').split(',')[-1]
					item['store_hours'] = ""
					hours = ""
					if 'HoursOfOperation' in  each_item:
						hours  = each_item['HoursOfOperation']
					for day in hours:
						value = hours[day];
						if (day != "TimeZone"):
							item['store_hours'] += day + ":" + value['Hours'][0]['OpenTime'] + "-" + value['Hours'][0]['CloseTime'] + ";"
					#item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = self.validate(store, 'ComingSoon')

					if item['store_number'] == "" or (store["LocationId"] != "" and store["LocationId"] in self.uid_list):
					    return
					self.uid_list.append(store["LocationId"])
					yield item

    def validate(self, store, attribute):
    	if attribute in store:
    		return store[attribute][0]
    	return ""


