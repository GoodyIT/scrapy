import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class Saelite(scrapy.Spider):
    name = "saelite"
    uid_list = []

    start_urls = ['http://storelocator.golfgalaxy.com/ajax?&xml_request=%3Crequest%3E%3Cappkey%3ECE23B360-C828-11E4-B146-ED9AA38844B8%3C%2Fappkey%3E%3Cformdata+id%3D%22locatorsearch%22%3E%3Cdataview%3Estore_default%3C%2Fdataview%3E%3Climit%3E5000%3C%2Flimit%3E%3Catleast%3E1%3C%2Fatleast%3E%3Cgeolocs%3E%3Cgeoloc%3E%3Caddressline%3E83101%3C%2Faddressline%3E%3Ccountry%3EUS%3C%2Fcountry%3E%3Clongitude%3E%3C%2Flongitude%3E%3Clatitude%3E%3C%2Flatitude%3E%3C%2Fgeoloc%3E%3C%2Fgeolocs%3E%3Csearchradius%3E3000%3C%2Fsearchradius%3E%3Cstateonly%3E100%3C%2Fstateonly%3E%3C%2Fformdata%3E%3C%2Frequest%3E', 'http://storelocator.golfgalaxy.com/ajax?&xml_request=%3Crequest%3E%3Cappkey%3ECE23B360-C828-11E4-B146-ED9AA38844B8%3C%2Fappkey%3E%3Cformdata+id%3D%22locatorsearch%22%3E%3Cdataview%3Estore_default%3C%2Fdataview%3E%3Climit%3E5000%3C%2Flimit%3E%3Catleast%3E1%3C%2Fatleast%3E%3Cgeolocs%3E%3Cgeoloc%3E%3Caddressline%3E83101%3C%2Faddressline%3E%3Ccountry%3EUS%3C%2Fcountry%3E%3Clongitude%3E%3C%2Flongitude%3E%3Clatitude%3E%3C%2Flatitude%3E%3C%2Fgeoloc%3E%3C%2Fgeolocs%3E%3Csearchradius%3E3000%3C%2Fsearchradius%3E%3Cstateonly%3E100%3C%2Fstateonly%3E%3C%2Fformdata%3E%3C%2Frequest%3E', 'http://storelocator.golfgalaxy.com/ajax?&xml_request=%3Crequest%3E%3Cappkey%3ECE23B360-C828-11E4-B146-ED9AA38844B8%3C%2Fappkey%3E%3Cformdata+id%3D%22locatorsearch%22%3E%3Cdataview%3Estore_default%3C%2Fdataview%3E%3Climit%3E5000%3C%2Flimit%3E%3Catleast%3E1%3C%2Fatleast%3E%3Cgeolocs%3E%3Cgeoloc%3E%3Caddressline%3E83101%3C%2Faddressline%3E%3Ccountry%3EUS%3C%2Fcountry%3E%3Clongitude%3E%3C%2Flongitude%3E%3Clatitude%3E%3C%2Flatitude%3E%3C%2Fgeoloc%3E%3C%2Fgeolocs%3E%3Csearchradius%3E3000%3C%2Fsearchradius%3E%3Cstateonly%3E111%3C%2Fstateonly%3E%3C%2Fformdata%3E%3C%2Frequest%3E']
    # get longitude and latitude for a state by using google map.
    def parse(self, response):
        stores = response.xpath("//poi")
        for store in stores:
            try:
                item = ChainItem()
                item['store_name'] = self.validate(store.xpath(".//name/text()"))
                item['store_number'] = self.validate(store.xpath(".//uid/text()")).replace('-','')
                item['address'] = self.validate(store.xpath(".//address1/text()"))
                item['address2'] = self.validate(store.xpath(".//address2/text()"))
                item['phone_number'] = self.validate(store.xpath(".//phone/text()"))
                item['city'] = self.validate(store.xpath(".//city/text()"))
                item['state'] = self.validate(store.xpath(".//province/text()"))
                if item['state'] == "":
                    item['state'] = self.validate(store.xpath(".//state/text()"))

                item['zip_code'] = self.validate(store.xpath(".//postalcode/text()"))
                item['country'] = self.validate(store.xpath(".//country/text()"))
                item['latitude'] = self.validate(store.xpath(".//latitude/text()"))
                item['longitude'] = self.validate(store.xpath(".//longitude/text()"))
                
                monday = "MON " + self.validate(store.xpath(".//mondayopen/text()"))[:2] + ":" + self.validate(store.xpath(".//mondayopen/text()"))[2:] + ' - ' + self.validate(store.xpath(".//mondayclose/text()"))[:2] + ":" + self.validate(store.xpath(".//mondayclose/text()"))[2:]
                tuesday = "TUE " + self.validate(store.xpath(".//tuesdayopen/text()"))[:2] + ":" + self.validate(store.xpath(".//tuesdayopen/text()"))[2:] + ' - ' + self.validate(store.xpath(".//tuesdayclose/text()"))[:2] + ":" + self.validate(store.xpath(".//tuesdayclose/text()"))[2:]
                wednesday = "WED " + self.validate(store.xpath(".//wednesdayopen/text()"))[:2] + ":" +  self.validate(store.xpath(".//wednesdayopen/text()"))[2:] + ' - ' + self.validate(store.xpath(".//wednesdayclose/text()"))[:2] + ":" + self.validate(store.xpath(".//wednesdayclose/text()"))[2:]
                thursday = "THU " + self.validate(store.xpath(".//thursdayopen/text()"))[:2] + ":" + self.validate(store.xpath(".//thursdayopen/text()"))[2:] + ' - ' + self.validate(store.xpath(".//thursdayclose/text()"))[:2] + ":" + self.validate(store.xpath(".//thursdayclose/text()"))[2:]
                friday = "FRI " + self.validate(store.xpath(".//fridayopen/text()"))[:2] + ":" + self.validate(store.xpath(".//fridayopen/text()"))[2:] + ' - ' + self.validate(store.xpath(".//fridayclose/text()"))[:2] + ":" + self.validate(store.xpath(".//fridayclose/text()"))[2:]
                saturday = "SAT " + self.validate(store.xpath(".//saturdayopen/text()"))[:2] + ":" + self.validate(store.xpath(".//saturdayopen/text()"))[2:] + ' - ' + self.validate(store.xpath(".//saturdayclose/text()"))[:2] + ":" + self.validate(store.xpath(".//saturdayclose/text()"))[2:]
                sunday = "SUN " + self.validate(store.xpath(".//sundayopen/text()"))[:2] + ":" + self.validate(store.xpath(".//sundayopen/text()"))[2:] + ' - ' + self.validate(store.xpath(".//sundayclose/text()"))[:2] + ":" + self.validate(store.xpath(".//sundayclose/text()"))[2:]

                item['store_hours'] = monday + "; " + tuesday + "; " + wednesday + "; " + thursday + "; "+ friday + "; "+ saturday + "; "+ sunday
                
                #item['store_type'] = info_json["@type"]
                item['other_fields'] = ""
                item['coming_soon'] = self.validate(store.xpath(".//openingsoon/text()"))

                if item["store_number"] != "" and item["store_number"] in self.uid_list:
                    return

                self.uid_list.append(item["store_number"])
                yield item
            except:
                continue

    # get store info in store detail page
    #def parse_store_content(self, response):
    #    pass

    def validate(self, xpath_obj):
        try:
            return xpath_obj.extract_first().strip()
        except:
            return ""


