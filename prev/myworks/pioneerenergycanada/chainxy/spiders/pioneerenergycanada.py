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

class Pioneerenergycanada(scrapy.Spider):
    name = "pioneerenergycanada"

    domain = "http://www.pioneer.ca/stations-services/station-locator?&cname=BizSearchResult&country=canada&state=on&fullcrit=york,%20ny,on&tag=All|All|All|All|All|All|All|All|All|All&m=20000"
    start_urls = ["http://www.pioneer.ca/stations-services/station-locator?&m=20&cname=BizProfileReadOnly&bizid=%s"]
    store_id = []

    def start_requests(self):
        for x in xrange(1, 149):
            yield scrapy.Request(url= "http://www.pioneer.ca/stations-services/station-locator?&m=20&cname=BizProfileReadOnly&bizid=%s" % x, callback=self.parse_store)

    def parse_store(self, response):
        item = ChainItem()

        item['store_number'] = ''
        item['store_name'] = self.validate(response.xpath('.//span[@id="dnn_ctr2860_ControlLoader_BizProfileReadOnly_lblBusinessName"]/text()').extract_first())
        if item['store_name'].strip() == '':
            return
        item['address2'] =  ''
        item['country'] = self.validate(response.xpath('.//span[@id="dnn_ctr2860_ControlLoader_BizProfileReadOnly_lblCountry"]/text()').extract_first())
        item['address'] = self.validate(response.xpath('.//span[@id="dnn_ctr2860_ControlLoader_BizProfileReadOnly_lblAddress"]/text()').extract_first())
        item['city'] = self.validate(response.xpath('.//span[@id="dnn_ctr2860_ControlLoader_BizProfileReadOnly_lblCity"]/text()').extract_first())
        item['state'] = self.validate(response.xpath('.//span[@id="dnn_ctr2860_ControlLoader_BizProfileReadOnly_lblState"]/text()').extract_first())
        item['zip_code'] = self.validate(response.xpath('.//span[@id="dnn_ctr2860_ControlLoader_BizProfileReadOnly_lblZip"]/text()').extract_first())
        item['phone_number'] = ''
        item['store_hours'] = self.validate(response.xpath('.//tr[@id="tris24"]/td/text()').extract_first())
        item['coming_soon'] = "0"
        item['store_hours'] = ''
        item['latitude'] =  response.xpath('.//input[@id="dnn_ctr2860_ControlLoader_BizProfileReadOnly_hdnLat"]/@value').extract_first()
        item['longitude'] = response.xpath('.//input[@id="dnn_ctr2860_ControlLoader_BizProfileReadOnly_hdnLong"]/@value').extract_first()
        item['other_fields'] = ''   
        yield item
            
    def validate(self, value):
        if value == None:
            return ""
        else:
            return value.strip()




        

