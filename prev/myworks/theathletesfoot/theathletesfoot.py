import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
from lxml import etree
import pdb

class TheathletesfootSpider(scrapy.Spider):
    name = "theathletesfoot"

    start_urls = ["http://www.theathletesfoot.com/api/sitecore/stores/search?lat1=-90&lon1=-180&lat2=90&lon2=180&sc_site=tafus"]
    storeNumbers = []

    def parse(self, response):
        stores = json.loads(response.body)
        for store in stores:
            try:
                item = ChainItem()
                item['store_name'] = store['Name']
                item['store_number'] = store['SitecoreId']
                item['address'] = store['AddressLine1']
                item['address2'] = store['AddressLine2']

                pdb.set_trace()
                if item['address2'][0].strip() != ' ' and item['address2'][0].isdigit() == True:
                    temp = item['address']
                    item['address'] = item['address2']
                    item['address2'] = temp

                item['phone_number'] = store['Phone'].replace(' ', '').replace('ext.', ' / ').replace('+', '')
                item['latitude'] = store['Latitude']
                item['longitude'] = store['Longitude']
                item['city'] = store['City']
                item['state'] = store['State']

                item['zip_code'] = store['ZipCode']
                item['country'] = store['Country']

                item['store_hours'] = ""
                #item['store_type'] = info_json["@type"]
                item['other_fields'] = ""
                item['coming_soon'] = '0'
                yield item
            except:
                pdb.set_trace()
                continue


