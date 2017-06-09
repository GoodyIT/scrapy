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

class Froots(scrapy.Spider):
    name = "froots"

    domain = "http://www.froots.com/"
    start_urls = ["http://www.froots.com/locations.html"]
    store_id = []

    internatioal_list = ["Dominican Republic", "Honduras", "Iraq", "Mexico", "Panama", "Turks & Caicos"]

    # calculate number of pages
    def parse(self, response):
        store_list = response.xpath('.//div[@class="col-md-12 locations1"]/div')
        for store_info in store_list:
            try:
                item = ChainItem()
                info = store_info.xpath('.//p//text()').extract()
                if len(info) <= 1:
                    continue

                info = [tp.strip().replace('\n', '').replace('\r', '') for tp in info if tp.strip() != ""]
          
                item['store_number'] = ''
                item['store_name'] = self.validate(info[0])
                item['address2'] = ''
                item['latitude'] = ''
                item['longitude'] = ''
                item['store_hours'] = ''
                item['other_fields'] = ""
                item['coming_soon'] = "0"

                if item['store_name'].strip() == ' ':
                    pdb.set_trace()

                country = store_info.xpath('.//h2/text()').extract_first()
                if country in self.internatioal_list:
                    item['country'] = country
                else:
                    item['country'] = 'United States'

                if len(info) == 8:
                    item['address'] = self.validate(info[0])
                    citystatezip = self.parse_citystatezip(info[1])
                    item['city'] = citystatezip[0]
                    item['state'] =  citystatezip[1]
                    item['zip_code'] =  citystatezip[2]
                    item['phone_number'] = self.validate(info[3])

                if len(info) == 7:
                    if country in self.internatioal_list:
                        item['city'] = self.validate(info[1].split(',')[0])
                        item['phone_number'] = self.validate(info[6])
                        item['address'] = self.validate(info[1])
                        item['address2'] =  self.validate(info[2])
                        item['state'] =  ''
                        item['zip_code'] =  ''
                    else:
                        try:
                            citystatezip = self.parse_citystatezip(info[1])
                            item['phone_number'] = self.validate(info[3])
                            item['address'] = self.validate(info[0])
                        except:
                            citystatezip = self.parse_citystatezip(info[2])
                            item['phone_number'] = self.validate(info[6])
                            item['address'] = self.validate(info[1])
                        item['city'] = citystatezip[0]
                        item['state'] =  citystatezip[1]
                        item['zip_code'] =  citystatezip[2]

                if len(info) == 6:
                    if country in self.internatioal_list:
                        item['address'] = self.validate(info[1])
                        item['state'] =  ''
                        item['zip_code'] =  ''
                        if country.find('Panama') == -1:
                            item['address2'] = self.validate(info[2])
                            item['city'] = self.validate(info[4])
                            item['phone_number'] = ''
                        elif country.find('Dominican') != -1:
                            item['address'] = self.validate(info[2])
                            item['address2'] = self.validate(info[1])
                            item['city'] = self.validate(info[3].split(',')[0])
                            item['phone_number'] = self.validate(info[-1])
                        else :
                            item['city'] = self.validate(info[2].split(',')[0])
                            item['phone_number'] = self.validate(info[5])
                    else:
                        try:
                            citystatezip = self.parse_citystatezip(info[2])
                            item['address'] = self.validate(info[0])
                            item['address2'] = self.validate(info[1])
                            item['phone_number'] = self.validate(info[5])
                         
                        except:
                            citystatezip = self.parse_citystatezip(info[1])
                            item['address'] = self.validate(info[0])
                            item['phone_number'] = self.validate(info[3])
                        item['city'] = citystatezip[0]
                        item['state'] =  citystatezip[1]
                        item['zip_code'] =  citystatezip[2]

                        if item['state'] == 'Guam':
                            item['phone_number'] = self.validate(info[4])
                if len(info) == 5:
                    if country in self.internatioal_list:
                        item['address'] = self.validate(info[0])
                        item['city'] = self.validate(info[1].split(',')[0])
                        item['phone_number'] = self.validate(info[3])
                    else:
                        citystatezip = ()
                        try:
                            citystatezip = self.parse_citystatezip(info[2])
                            item['address'] = self.validate(info[1])
                        except:
                            citystatezip = self.parse_citystatezip(info[1])
                            item['address'] = self.validate(info[0])
                        item['city'] = citystatezip[0]
                        item['state'] =  citystatezip[1]
                        item['zip_code'] =  citystatezip[2]
                        item['phone_number'] = self.validate(info[-1])
                    
                elif len(info) == 4:
                    if country in self.internatioal_list:
                        item['address'] = self.validate(info[0])
                        item['city'] = self.validate(info[1].split(',')[0])
                        item['phone_number'] = self.validate(info[-1])
                    else:
                        item['address'] = self.validate(info[0])
                        citystatezip = self.parse_citystatezip(info[1])
                        item['city'] = citystatezip[0]
                        item['state'] =  citystatezip[1]
                        item['zip_code'] =  citystatezip[2]
                        item['phone_number'] = self.validate(info[-1])

                elif len(info) == 3:
                    item['state'] = ''
                    item['zip_code'] = ''
                    item['phone_number'] = ''
                    item['city'] = self.validate(info[2].split(',')[0])
                    if info[2].find('Panama') != -1:
                        item['address'] = self.validate(info[1])
                    elif info[1].find('Phone') != -1:
                        item['address'] = self.validate(info[0].split(',')[0])
                        item['city'] = self.validate(info[0].split(',')[1])
                        item['phone_number'] = self.validate(info[-1])
                    else:
                        item['address'] = self.validate(info[1])

                elif len(info) == 2:
                    if country in self.internatioal_list:
                        item['city'] = self.validate(info[1].split(',')[0])
                        item['state'] = ''
                        item['zip_code'] = ''
                        item['address'] = self.validate(info[0])
                        item['phone_number'] = ''
                    else:
                        citystatezip = self.parse_citystatezip(info[1])
                        item['city'] = citystatezip[0]
                        item['state'] =  citystatezip[1]
                        item['zip_code'] =  citystatezip[2]
                        item['address'] = self.validate(info[0])
                        item['phone_number'] = ''

                if item['store_name'] == item['address'] or item['store_name'].find('Piedras.') != -1:
                    item['store_name'] = store_info.xpath('.//h3/text()').extract_first()
                if item['store_name'].find('(Coming Soon)') != -1:
                    item['store_name'] = item['store_name'].replace("(Coming Soon)", "")
                    item['coming_soon'] = "1"
                if item['address'].find('Building 9025') != -1:
                    pdb.set_trace()

                yield item
            except:
                pdb.set_trace()

    def validate(self, value):
        if value != None:
            return value.strip().encode('utf8').replace('\xc2\xa0', '').replace('\xc3\xada', 'ia').replace('\xc3\xa9', 'e').replace('\xc3\xb3', 'o')
        else:
            return ""

    def parse_citystatezip(self, value):
        city = self.validate(value.split(',')[0])
        state = self.validate(value.split(',')[1].strip().split(' ')[0])
        zip_code = self.validate(value.split(',')[1].strip().split(' ')[-1])
        return (city, state, zip_code)





        

