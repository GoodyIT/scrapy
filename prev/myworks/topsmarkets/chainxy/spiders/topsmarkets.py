import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem

from geopy.geocoders import Nominatim

class Topsmarkets(scrapy.Spider):
    name = "topsmarkets"

    domain = "http://www.topsmarkets.com"
    start_urls = ["http://www.topsmarkets.com/StoreLocator/Store_MapLocation_S.las?State=all"]
    store_link = 'http://www.topsmarkets.com/StoreLocator/Store?L=%s&M=&From=&S='
    store_id = []

    def __init__(self):
        self.geolocator = Nominatim()

    # calculate number of pages
    def parse(self, response):
        data=json.loads(response.body)
        for shop_info in data:
            url = self.store_link % shop_info['StoreNbr']
            request = scrapy.Request(url=url, callback=self.parse_store_contents)
            request.meta['store_number'] = shop_info['StoreNbr'];
            request.meta['lat'] = shop_info['Latitude']
            request.meta['lng'] = shop_info['Longitude']
            yield request

    # pare store detail page
    def parse_store_contents(self, response):   
        store = response.xpath("//div[contains(@class, 'contact_information BasicInfo-BS')]")
        item = ChainItem()
        item['store_name'] = response.xpath("//h2/text()")
        item['store_number'] = response.meta["store_number"]
        address = store.xpath("//p[contains(@class, 'Address')]/text()").extract()
        for value in address:
            if value.strip() != "":
                item['address'] = value.strip()
                break
        
        item['address2'] = ''
        
        item['phone_number'] = store.xpath("//p[contains(@class, 'PhoneNumber')]/text()").extract_first().strip()
        item['latitude'] = response.meta["lat"]
        item['longitude'] = response.meta["lng"]
        location = self.geolocator.reverse("%s, %s" % (str(item['latitude']), str(item['longitude'])))

        try:
            item['city'] = location.raw["address"]["city"]
        except:
            if 'town' in location.raw["address"]:
                item['city'] = location.raw["address"]["town"]

        item['state'] = location.raw["address"]["state"] if "state" in location.raw["address"] else ""
        item['zip_code'] = location.raw["address"]["postcode"]
        item['country'] = location.raw["address"]["country_code"].upper()
        
        item['store_hours'] = self.validate(store.xpath(".//dd/text()"))
        
        #item['store_type'] = info_json["@type"]
        item['other_fields'] = ""
        item['coming_soon'] = "0"

        yield item

    def validate(self, xpath_obj):
        try:
            return xpath_obj.extract_first().strip()
        except:
            return ""

        

