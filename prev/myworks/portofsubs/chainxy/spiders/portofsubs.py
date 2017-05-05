import scrapy
import json
import re
import csv
import requests
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem

class Portofsubs(scrapy.Spider):
    name = "portofsubs"

    domain = "http://www.portofsubs.com/"
    start_urls = ["http://portofsubs.com/wp-content/plugins/store-locator/sl-xml.php?mode=gen&lat=35.3732921&lng=-119.01871249999999&radius=1000"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_list = response.xpath("//markers/marker")
        for store in store_list:
            item = ChainItem()
            
            item['store_name'] = store.xpath(".//@name").extract_first()
            
            if item['store_name'].find(u'\u2014') != -1:
                item['store_name'] = item['store_name'].split(u'\u2014')[0]

            if item['store_name'].find('-') != -1:
                item['store_name'] = item['store_name'].split('-')[0]

            item['store_number'] = item['store_name'].split('#')[1].strip()    
            item['city'] = store.xpath(".//@city").extract_first()
            item['state'] = store.xpath(".//@state").extract_first()
            item['zip_code'] = store.xpath(".//@zip").extract_first()
            item['address'] = self.validate(store.xpath(".//@street").extract_first())
            item['address2'] = self.validate(store.xpath(".//@street2").extract_first())
            item['country'] = 'United States'
            item['phone_number'] = store.xpath(".//@phone").extract_first()
            item['latitude'] = store.xpath(".//@lat").extract_first()
            item['longitude'] = store.xpath(".//@lng").extract_first()
            
            item['store_hours'] = store.xpath(".//@hours").extract_first()
            item['other_fields'] = ""
            item['coming_soon'] = "0"
                
            yield item


    def validate(self, value):
        return value.replace('&#39;', "'").replace('&#44;', ',').replace('&amp;', '&').replace(u'\u2013', '-')





        

