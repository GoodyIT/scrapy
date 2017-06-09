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
import usaddress

class Atrias(scrapy.Spider):
    name = "atrias"

    domain = "http://atrias.com/wp/locations/"
    start_urls = ["http://atrias.com/wp/locations/"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//div[contains(@class, "vc_col-sm-6 wpb_column column_container vc_column_container col boxed centered-text no-extra-padding")]//div[contains(@class, "wpb_text_column wpb_content_element")]')
        for store in store_list:
            try:
                item = ChainItem()
                
                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                item['store_name'] = self.validate(store.xpath('.//h2/text()').extract_first())
                if item['store_name'] == '':
                    continue
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                info = store.xpath('.//p[1]//text()').extract()
                info = [tp.strip().replace('\n', '').replace('\r', '') for tp in info if tp.strip() != ""]
                idx = 0
                for x, value in enumerate(info):
                    if value.find('Phone') != -1:
                        idx = x

                addr = usaddress.parse(" ".join(info[:idx]))
                city = state = zip_code = street = ''
                for temp in addr:
                    if temp[1] == 'PlaceName':
                        city += temp[0].replace(',','') + ' '
                    elif temp[1] == 'StateName':
                        state = temp[0].replace(',','')
                    elif temp[1] == 'ZipCode':
                        zip_code = temp[0].replace(',','')
                    else:
                        street += temp[0].replace(',','') + ' '
                item['address'] = street
                item['city'] = city
                item['state'] =  state
                item['zip_code'] =  zip_code
                item['address2'] = ''
                item['phone_number'] =  info[idx+1]
                hours = store.xpath('.//p')
                item['store_hours'] = ''
                for hour in hours[2:-1]:
                    temp = hour.xpath('.//text()').extract();
                    temp = [tp.strip().replace('\n', '').replace('\r', '') for tp in temp if tp.strip() != ""]      
                    temp = ':'.join(temp) + '; '
                    if temp.find('Closing') != -1:
                        continue             
                    item['store_hours'] +=  temp

                item['store_hours'] = self.validate(item['store_hours'])
          
                # if item['address'].find('103 Federal Street') != -1:
                #     pdb.set_trace()
                yield item
            except:
                pdb.set_trace()
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2013', '-').replace(u'\u2019', '-').encode('utf8').replace('\xc2\xa0', '')
        else:
            return ""





        

