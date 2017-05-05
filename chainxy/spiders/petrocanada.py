import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import XMLFeedSpider
from chainxy.items import ChainItem
import pdb
import re
from lxml import html
from lxml.html import fromstring
from lxml import etree

class PetrocanadaSpider(scrapy.Spider):
	name = "petrocanada"
	uid_list = []
	states_list = []
	headers = {"Content-Type" : "application/x-www-form-urlencoded"}
	request_url_for_gas_station = "http://www.petro-canada.ca/services/4146.aspx?P=%s&B=&SI=%s" #SI:count
	request_url_for_truck_stop = "http://www.petro-canada.ca/services/6197.aspx?P=%s&B=&SI=%s"
	request_url_for_fuel_distributor = "http://www.petro-canada.ca/en/business/find-a-fuel-distributor.aspx"

	def __init__(self):
	  place_file = open('citiesusca.json', 'rb')
	  self.cities_list = json.load(place_file)

	def start_requests(self):
		for row in self.cities_list:
			if self.cities_list[row]['country'] == 'Canada':
				#Fuel Distributor
				if self.cities_list[row]['state'] not in self.states_list:
					self.states_list.append(self.cities_list[row]['state'])
					form_data = {
						'id5684:_ctl0:ddlProvince' : self.cities_list[row]['state'],
						'm' : 'r',
						'id5684:_ctl0:ddlCity' : ''
					}
					yield FormRequest(url=self.request_url_for_fuel_distributor,
		                    formdata=form_data,
		                    headers=self.headers,
		                    callback=self.parseStoreForFuelDistributor)
					#Gas Station
					request_url = self.request_url_for_gas_station % (self.cities_list[row]['state'], 0)
					request = scrapy.Request(url=request_url,
		                    callback=self.parseStoreForGasStation)
					request.meta['state'] = self.cities_list[row]['state']
					yield request
					#Truck Stop
					request_url = self.request_url_for_truck_stop % (self.cities_list[row]['state'], 0)
					request = scrapy.Request(url=request_url,
		                    callback=self.parseStoreForTruckStop)
					request.meta['state'] = self.cities_list[row]['state']
					yield request

	# Gas Station
	def parseStoreForGasStation(self, response):
		info = html.fromstring(response.body)
		for store in info.xpath('//location'):
			item = ChainItem()
			item['store_name'] = ""
			item['store_number'] = store.xpath('./entityid/text()')[0]
			item['address'] = store.xpath('./addressline/text()')[0]
			item['address2'] = ""
			item['phone_number'] = store.xpath('./phone/text()')[0]
			item['city'] = store.xpath('./primarycity/text()')[0]
			item['state'] = store.xpath('./subdivision/text()')[0]
			item['zip_code'] = store.xpath('./postalcode/text()')[0]
			item['country'] = store.xpath('./countryregion/text()')[0]
			item['latitude'] = store.xpath('./latitude/text()')[0]
			item['longitude'] = store.xpath('./longitude/text()')[0]
			item['store_hours'] = ""  
			#item['store_type'] = info_json["@type"]
			item['other_fields'] = ""
			item['coming_soon'] = ""
			if item['store_number'] != "" and item["store_number"] in self.uid_list:
			  continue
			self.uid_list.append(item["store_number"])
			request = scrapy.Request("http://www.petro-canada.ca/en/locations/find-a-gas-station.aspx?MODE=DTS&ID=%s" % (item['store_number']),
			                         callback=self.addHoursToStoreForGasStation)
			request.meta['item'] = item			
			yield request
		# For next page request
		total_count = int(info.xpath('./@count')[0])
		start_index = int(info.xpath('./@startindex')[0])
		if (start_index + len(info.xpath('//location'))) < total_count:
			request_url = self.request_url_for_gas_station % (response.meta['state'], len(info.xpath('//location')) + start_index)
			request = scrapy.Request(url=request_url,
				                    callback=self.parseStoreForGasStation)
			request.meta['state'] = response.meta['state']
			yield request

	def addHoursToStoreForGasStation(self, response):
		item = response.meta['item']
		hour_list = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
		for hour in hour_list:
			item["store_hours"] += hour + ":" + response.xpath('//span[contains(@id, "hoursOfOperation")]/text()').extract()[hour_list.index(hour)] + ";"
		yield item

	# Truck Store
	def parseStoreForTruckStop(self, response):
		info = html.fromstring(response.body)
		for store in info.xpath('//location'):
			item = ChainItem()
			item['store_name'] = ""
			item['store_number'] = store.xpath('./entityid/text()')[0]
			item['address'] = store.xpath('./addressline/text()')[0]
			item['address2'] = ""
			item['phone_number'] = store.xpath('./phone/text()')[0]
			item['city'] = store.xpath('./primarycity/text()')[0]
			item['state'] = store.xpath('./subdivision/text()')[0]
			item['zip_code'] = store.xpath('./postalcode/text()')[0]
			item['country'] = "Canada"
			item['latitude'] = store.xpath('./latitude/text()')[0]
			item['longitude'] = store.xpath('./longitude/text()')[0]
			item['store_hours'] = ""  
			#item['store_type'] = info_json["@type"]
			item['other_fields'] = ""
			item['coming_soon'] = ""
			if item['store_number'] != "" and item["store_number"] in self.uid_list:
			  continue
			self.uid_list.append(item["store_number"])
			request = scrapy.Request("http://www.petro-canada.ca/en/business/find-a-petro-pass-location.aspx?MODE=DTS&ID=%s" % (item['store_number']),
			                         callback=self.addHoursToStoreForTruckStop)
			request.meta['item'] = item			
			yield request
		# For next page request
		total_count = int(info.xpath('./@count')[0])
		start_index = int(info.xpath('./@startindex')[0])
		if (start_index + len(info.xpath('//location'))) < total_count:
			request_url = self.request_url_for_truck_stop % (response.meta['state'], len(info.xpath('//location')) + start_index)
			request = scrapy.Request(url=request_url,
				                    callback=self.parseStoreForTruckStop)
			request.meta['state'] = response.meta['state']
			yield request

	def addHoursToStoreForTruckStop(self, response):
		item = response.meta['item']
		hour_list = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
		for hour in hour_list:
			item["store_hours"] += hour + ":" + response.xpath('//span[contains(@id, "hoursOfOperation")]/text()').extract()[hour_list.index(hour)] + ";"
		yield item

	# Fuel Distributor.
	def parseStoreForFuelDistributor(self, response):
		try:
			stores = response.xpath('//td[@class="contentbox bodytext"]/span[1]/table[3]//table[1]//tr')		
			for store in stores:
				item = ChainItem()
				if self.validate(store.xpath('./td[@class="bodytext"][2]/a[1]/text()')):
					item['store_name'] = self.validate(store.xpath('./td[@class="bodytext"][2]/a[1]/text()'))
					item['store_number'] = ""
					item['address'] = ""
					item['address2'] = ""
					item['phone_number'] = store.xpath('.//span[contains(@id,"spanTelephone")]/text()').extract_first().split(':')[1].strip()
					item['city'] = ""
					for iter in store.xpath('./td[@class="bodytext"][2]/text()').extract():
						if iter.strip() != "":
							item['address'] = iter.split(',')[0].strip()
							item['city'] = iter.split(',')[1].strip()
					if item['city']:
						city_info = self.getCityInfo(item['city'])
						item['state'] = city_info['state']
						item['zip_code'] = city_info['zip_code']
						item['country'] = city_info['country']
						item['latitude'] = city_info['latitude']
						item['longitude'] = city_info['longitude']
					item['store_hours'] = ""
					# item['store_type'] = info_json["@type"]
					item['other_fields'] = ""
					item['coming_soon'] = ""
					yield item
		except:
			pass

	def getCityInfo(self, city):
		if city in self.cities_list:
			return self.cities_list[city]
		else:
			for city_item in self.cities_list:
				if city in city_item.upper():
					return self.cities_list[city_item]
			return {}

	def validate(self, xpath_obj):
		try:
			return xpath_obj.extract_first().strip()
		except:
			return ""

	def replaceWithNone(self, str):
		try:
			return str.encode('utf-8').replace('\r', '').replace('\n','').replace('\t','').replace('\xc2\xa0', ' ').strip()
		except:
			return ""

	def validate_re(self, str):
		try:
			return str.replace("'", "")
		except:
			""