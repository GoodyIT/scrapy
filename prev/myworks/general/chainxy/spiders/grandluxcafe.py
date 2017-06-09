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

import pdb

class Grandluxcafe(scrapy.Spider):
    name = "grandluxcafe"

    domain = "http://locations.grandluxcafe.com/fl/aventura/9/"
    start_urls = ["http://locations.grandluxcafe.com/fl/aventura/9/"]
    store_id = []

    def parse(self, response):
        ids = response.xpath('.//ul/li[@class="accordion-item"]/@id').extract()
        # pdb.set_trace()
        for _id in ids:
            yield scrapy.Request(url='http://locations.grandluxcafe.com/ajax?&xml_request=%3Crequest%3E%3Cappkey%3E6AE61B08-BDDD-11E4-91AA-0BADF48ECC77%3C%2Fappkey%3E%3Cformdata+id%3D%22getlist%22%3E%3Corder%3Ecity%3C%2Forder%3E%3Cobjectname%3ELocator%3A%3ABase%3C%2Fobjectname%3E%3Cwhere%3E%3Cstate%3E%3Ceq%3E'+_id.upper()+'%3C%2Feq%3E%3C%2Fstate%3E%3C%2Fwhere%3E%3C%2Fformdata%3E%3C%2Frequest%3E'  , callback=self.parse_store)

    def parse_store(self, response):
        store_list = response.xpath('.//poi')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = ''
            item['country'] = 'United States'
            item['latitude'] = store.xpath('.//latitude/text()').extract_first()
            item['longitude'] = store.xpath('.//longitude/text()').extract_first()
            item['store_name'] = store.xpath('.//name/text()').extract_first()
            item['other_fields'] = ""
            
            item['coming_soon'] = store.xpath('.//comingsoon/text()').extract_first()
            item['address'] = store.xpath('.//address1/text()').extract_first()
            item['address2'] = self.validate(store.xpath('.//address2/text()').extract_first())
            item['city'] = store.xpath('.//city/text()').extract_first()
            item['state'] = store.xpath('.//state/text()').extract_first()
            item['zip_code'] = store.xpath('.//postalcode/text()').extract_first()
            item['phone_number'] =  store.xpath('.//phone/text()').extract_first()

            item['store_hours'] = store.xpath('.//hourslabel1/text()').extract_first() + ':' + store.xpath('.//hoursfromto1/text()').extract_first() + '; ' + store.xpath('.//hourslabel2/text()').extract_first() + ':' + store.xpath('.//hoursfromto2/text()').extract_first() + '; ' + store.xpath('.//hourslabel3/text()').extract_first() + ':' + store.xpath('.//hoursfromto3/text()').extract_first() + '; ' + store.xpath('.//hourslabel4/text()').extract_first() + ':' + store.xpath('.//hoursfromto4/text()').extract_first() + '; '

            yield item
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

