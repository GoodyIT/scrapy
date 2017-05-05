import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem

from geopy.geocoders import Nominatim
import pdb

class Pizzanova(scrapy.Spider):
    name = "pizzanova"

    domain = "http://www.pizzanova.com/"
    start_urls = ["https://pizzanova.com/store-locator/?city=Aurora"]
    store_id = []
    loc_list = {}

    def __init__(self):
        self.geolocator = Nominatim()   

    # calculate number of pages
    def parse(self, response):
        geo_list = response.body.split('var PNStores = [["')[1].strip().split(']];var')[0].strip().split(',["')
        for geo in geo_list:
            name = geo.split('"')[0].strip()
            if len(geo.split('"')) == 3:
                name = geo.split('"')[1].strip()
                lat = geo.split(',')[0].strip()
                lng = geo.split(',')[1].strip()[:-1]
            else:
                lat = geo.split('"')[1].strip().split(',')[1].strip()
                lng = geo.split('"')[1].strip().split(',')[2].strip()[:-1]
            self.loc_list[name] = {"lat": lat, "lng": lng}
        
        city_list = response.xpath('//select[@id="mychange"]/option/text()').extract()
        for city in city_list:
            if city == 'Ajax' or city == 'Please select a city':
                continue
            url = "https://pizzanova.com/store-locator/?city=" + city
            yield scrapy.Request(url=url, callback=self.parse_store_contents)

    # pare store detail page
    def parse_store_contents(self, response): 

        store_list = response.xpath("//div[contains(@class, 'location-information')]")
        for store in store_list:
            try:
                item = ChainItem()
                item['store_name'] = store.xpath('.//h2/text()').extract_first()
                item['store_number'] = ''
                item['address'] = store.xpath('.//p/text()').extract_first()
                item['address2'] = ''
                item['phone_number'] = ''

                item['latitude'] = self.loc_list[item['store_name']]['lat']
                item['longitude'] = self.loc_list[item['store_name']]['lng']

                location = self.geolocator.reverse("%s, %s" % (str(item['latitude']), str(item['longitude'])))

                try:
                    item['city'] = location.raw["address"]["city"]
                except:
                    if 'town' in location.raw["address"]:
                        item['city'] = location.raw["address"]["town"]

                item['state'] = location.raw["address"]["state"] if "state" in location.raw["address"] else ""
                try:
                    item['zip_code'] = location.raw["address"]["postcode"]
                except:
                    item['zip_code'] = ''
                item['country'] = 'Canada'
               
                item['store_hours'] = ''
                hours = store.extract().split('<br>')
                for hour in hours:
                    if hour.find('div') != -1:
                        continue
                    item['store_hours'] += hour + "; "
                
                
                #item['store_type'] = info_json["@type"]
                item['other_fields'] = ""
                item['coming_soon'] = "0"
            except:
                pdb.set_trace()

            yield item

    def validate(self, xpath_obj):
        
        try:
            return xpath_obj.extract_first().strip()
        except:
            return ""

        

