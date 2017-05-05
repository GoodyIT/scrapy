import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb
from geopy.geocoders import Nominatim

class Logansroadhouse(scrapy.Spider):
	name = "logansroadhouse"
	uid_list = []
	domain = "http://logansroadhouse.com/"
 	store_url = "http://logansroadhouse.com/wp-admin/admin-ajax.php"
		
	headers = { 'Content-Type' : 'application/x-www-form-urlencoded', 'Accept': '*/*' }

	def __init__(self):
		self.geolocator = Nominatim()

	def start_requests(self):
		form_data = {
					'address': '',
					'formdata':'addressInput=',
					'lat':'37.09024',
					'lng':'-95.71289100000001',
					'name': '',
					'options[ignore_radius]':'0',
					'options[map_domain]':'maps.google.com',
					'options[no_autozoom]':'0',
					'options[no_homeicon_at_start]':'1',
					'options[radius_behavior]':'always_use',
					'options[use_sensor]':'0',
					'options[distance_unit]':'miles',
					'options[radii]':'10,25,50,(100),200,500',
					'options[map_center]':'United States',
					'options[map_center_lat]':'37.09024',
					'options[map_center_lng]':'-95.712891',
					'options[zoom_level]':'4',
					'options[zoom_tweak]':'0',
					'options[map_type]':'roadmap',
					'options[maplayout]':'[slp_mapcontent][slp_maptagline]',
					'options[map_home_icon]':'http://logansroadhouse.com/wp-content/plugins/store-locator-le/images/icons/blank.png',
					'options[map_end_icon]':'http://logansroadhouse.com/wp-content/plugins/store-locator-le/images/icons/bulb_azure.png',
					'options[immediately_show_locations]':'1',
					'options[initial_radius]':'5000',
					'options[initial_results_returned]':'250',
					'options[message_no_results]':'No locations found.',
					'options[label_website]':'Website',
					'options[label_directions]':'Directions',
					'options[label_email]':'Email',
					'options[label_phone]':'Phone:',
					'options[label_fax]':'Fax:' ,
					'options[map_width]':'100',
					'options[theme]': '',
					'options[id]': '',
					'options[hide_search_form]':'',
					'options[force_load_js]':'0',
					'options[map_region]':'us',
					'radius':'5000',
					'tags': '',
					'action':'csl_ajax_onload',
				}

		request = FormRequest(url=self.store_url,
				              formdata=form_data,
				              headers=self.headers,
				              callback=self.parse_store)
		yield request
	
	def parse_store(self, response):
		stores = json.loads(response.body)['response']
		for store in stores:
			item = ChainItem()

			item['store_number'] = store['data']['sl_id']
			item['store_name'] = store['name']
			item['address'] = store['address']
			item['address2'] = store['address2']
			item['phone_number'] = store['phone']
			item['latitude'] = store['lat']
			item['longitude'] = store['lng']
			item['city'] = store['city']
			item['state'] = store['state']
			item['zip_code'] = store['zip']
			item['country'] = store['country']
			item['other_fields'] = ""
			item['store_hours'] = store['data']['sl_hours'].replace('\r\n',';')
			item['coming_soon'] = 0

			yield item

	