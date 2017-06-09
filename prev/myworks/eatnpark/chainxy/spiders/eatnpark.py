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

class Eatnpark(scrapy.Spider):
    name = "eatnpark"

    domain = "http://www.eatnpark.com/"
    start_urls = ["http://hosted.where2getit.com/eatnpark/ajax?&xml_request=%3Crequest%3E%3Cappkey%3E90D3A4D8-B844-3CAC-BD6F-79DDE6FAF9BC%3C%2Fappkey%3E%3Cformdata+id%3D%22locatorsearch%22%3E%3Cdataview%3Estore_default%3C%2Fdataview%3E%3Cgeolocs%3E%3Cgeoloc%3E%3Caddressline%3E%3C%2Faddressline%3E%3Clongitude%3E-69.48587400667206%3C%2Flongitude%3E%3Clatitude%3E43.765893546463275%3C%2Flatitude%3E%3C%2Fgeoloc%3E%3C%2Fgeolocs%3E%3Csearchradius%3E2669.906249999999%3C%2Fsearchradius%3E%3Cwhere%3E%3Cpickup_window%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fpickup_window%3E%3Cmeeting_room%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fmeeting_room%3E%3Cflag24hour%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fflag24hour%3E%3C%2Fwhere%3E%3C%2Fformdata%3E%3C%2Frequest%3E"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_list = response.xpath('//response/collection/poi')
        for store_info in store_list:
            item = ChainItem()

            item['store_number'] = store_info.xpath('.//uid/text()').extract_first()
            item['store_name'] = store_info.xpath('.//name/text()').extract_first()
            item['city'] = store_info.xpath('.//city/text()').extract_first()
            item['state'] = store_info.xpath('.//state/text()').extract_first()
            item['zip_code'] = store_info.xpath('.//postalcode/text()').extract_first()
            item['address'] = store_info.xpath('.//address1/text()').extract_first()
            item['address2'] = store_info.xpath('.//address2/text()').extract_first()
            item['country'] = 'United States'
            item['phone_number'] = store_info.xpath('.//phone/text()').extract_first()
            item['latitude'] = store_info.xpath('.//latitude/text()').extract_first()
            item['longitude'] = store_info.xpath('.//longitude/text()').extract_first()
            item['store_hours'] = store_info.xpath('.//open24h/text()').extract_first().split('<')[0].strip()
            item['other_fields'] = ""
            item['coming_soon'] = "0"
                
            yield item


    def validate(self, value):
        if type(value) == "str":
            return value
        else:
            return ""





        

