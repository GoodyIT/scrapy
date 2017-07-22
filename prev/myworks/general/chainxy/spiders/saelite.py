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
from lxml import html

class Saelite(scrapy.Spider):
    name = "saelite"

    domain = "https://www.dickssportinggoods.com"
    start_urls = ["https://storelocator.dickssportinggoods.com/responsive/ajax?&xml_request=%3Crequest%3E%3Cappkey%3E17E8F19C-098E-11E7-AC2C-11ACF3F4F7A7%3C%2Fappkey%3E%3Cformdata+id%3D%22locatorsearch%22%3E%3Cdataview%3Estore_default%3C%2Fdataview%3E%3Climit%3E5000%3C%2Flimit%3E%3Catleast%3E10%3C%2Fatleast%3E%3Cgeolocs%3E%3Cgeoloc%3E%3Caddressline%3E%3C%2Faddressline%3E%3Ccountry%3E%3C%2Fcountry%3E%3Clongitude%3E-101.48187248655391%3C%2Flongitude%3E%3Clatitude%3E40.21870500843178%3C%2Flatitude%3E%3C%2Fgeoloc%3E%3C%2Fgeolocs%3E%3Csearchradius%3E2000%3C%2Fsearchradius%3E%3Cwhere%3E%3Cbrandname%3E%3Ceq%3EDicks+Sporting+Goods%3C%2Feq%3E%3C%2Fbrandname%3E%3C%2Fwhere%3E%3C%2Fformdata%3E%3C%2Frequest%3E"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//poi')
        for store in store_list:
            item = ChainItem()
            item['store_number'] = self.validate(store.xpath(".//uid/text()")).replace('-','')
            if item['store_number'] in self.store_id:
                continue
            self.store_id.append(item['store_number'])
            if self.validate(store.xpath('.//country/text()')).find('US') != -1:
                item['country'] = 'United States'
            else:
                item['country'] = self.validate(store.xpath('.//country/text()'))
                
            item['latitude'] = self.validate(store.xpath('.//latitude/text()'))
            item['longitude'] = self.validate(store.xpath('.//longitude/text()'))
            item['store_name'] = self.validate(store.xpath('.//name/text()'))
            item['other_fields'] = ""
            item['coming_soon'] = self.validate(store.xpath(".//openingsoon/text()"))
            item['address'] = self.validate(store.xpath('.//address1/text()'))
            item['address2'] = self.validate(store.xpath('.//address2/text()'))
            item['city'] = self.validate(store.xpath('.//city/text()'))
            item['state'] = self.validate(store.xpath('.//state/text()'))
            item['zip_code'] = self.validate(store.xpath('.//postalcode/text()'))
            item['phone_number'] =  self.validate(store.xpath('.//phone/text()'))

            monday = "MON " + self.validate(store.xpath(".//mondayopen/text()"))[:2] + ":" + self.validate(store.xpath(".//mondayopen/text()"))[2:] + ' - ' + self.validate(store.xpath(".//mondayclose/text()"))[:2] + ":" + self.validate(store.xpath(".//mondayclose/text()"))[2:]
            tuesday = "TUE " + self.validate(store.xpath(".//tuesdayopen/text()"))[:2] + ":" + self.validate(store.xpath(".//tuesdayopen/text()"))[2:] + ' - ' + self.validate(store.xpath(".//tuesdayclose/text()"))[:2] + ":" + self.validate(store.xpath(".//tuesdayclose/text()"))[2:]
            wednesday = "WED " + self.validate(store.xpath(".//wednesdayopen/text()"))[:2] + ":" +  self.validate(store.xpath(".//wednesdayopen/text()"))[2:] + ' - ' + self.validate(store.xpath(".//wednesdayclose/text()"))[:2] + ":" + self.validate(store.xpath(".//wednesdayclose/text()"))[2:]
            thursday = "THU " + self.validate(store.xpath(".//thursdayopen/text()"))[:2] + ":" + self.validate(store.xpath(".//thursdayopen/text()"))[2:] + ' - ' + self.validate(store.xpath(".//thursdayclose/text()"))[:2] + ":" + self.validate(store.xpath(".//thursdayclose/text()"))[2:]
            friday = "FRI " + self.validate(store.xpath(".//fridayopen/text()"))[:2] + ":" + self.validate(store.xpath(".//fridayopen/text()"))[2:] + ' - ' + self.validate(store.xpath(".//fridayclose/text()"))[:2] + ":" + self.validate(store.xpath(".//fridayclose/text()"))[2:]
            saturday = "SAT " + self.validate(store.xpath(".//saturdayopen/text()"))[:2] + ":" + self.validate(store.xpath(".//saturdayopen/text()"))[2:] + ' - ' + self.validate(store.xpath(".//saturdayclose/text()"))[:2] + ":" + self.validate(store.xpath(".//saturdayclose/text()"))[2:]
            sunday = "SUN " + self.validate(store.xpath(".//sundayopen/text()"))[:2] + ":" + self.validate(store.xpath(".//sundayopen/text()"))[2:] + ' - ' + self.validate(store.xpath(".//sundayclose/text()"))[:2] + ":" + self.validate(store.xpath(".//sundayclose/text()"))[2:]

            item['store_hours'] = monday + "; " + tuesday + "; " + wednesday + "; " + thursday + "; "+ friday + "; "+ saturday + "; "+ sunday
                
            yield item
    
    def validate(self, xpath_obj):
        try:
            return xpath_obj.extract_first().strip()
        except:
            return ""






        

