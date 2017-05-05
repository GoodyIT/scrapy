import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem

class Pollotropical(scrapy.Spider):
	name = "pollotropical"
	uid_list = []
	domain = "http://pollotropical.com/"
 	store_url = "http://pollotropical.com/wp-admin/admin-ajax.php?action=get_ajax_processor&processor=get-locations&queryType=&postID=20&slug=locator&stores="
		
	def start_requests(self):
		yield scrapy.Request(url=self.store_url, callback=self.parse_store)
	
	def parse_store(self, response):
		stores = json.loads(response.body)
		for store in stores:
			item = ChainItem()

			item['store_number'] = store['locator_store_number']
			item['store_name'] = store['post_title']
			item['address'] = store['street_address_1'].replace('<br>', ' ')
			item['address2'] = store['street_address_2']
			item['phone_number'] = store['phone_number']
			item['latitude'] = store['x_coordinate']
			item['longitude'] = store['y_coordinate']
			item['city'] = store['city']
			item['state'] = store['state']
			item['zip_code'] = store['zip_code']
			item['country'] = store['locator_country']
			item['other_fields'] = ""
			item['store_hours'] = store['hours'].replace('<br>', ';')
			item['coming_soon'] = 0

			yield item

	