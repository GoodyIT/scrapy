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

class Freshcity(scrapy.Spider):
    name = "freshcity"

    domain = "https://freshcity.com/"
    start_urls = ["https://freshcity.com/locations/"]
    store_id = []
    idx = 0

    def parse(self, response):
        store_list = response.xpath('.//div[@class="vc_row wpb_row vc_row-fluid "]')[2:]
        name_list = response.xpath('.//div[@class="entry-content"]//div[@class="wpb_gmaps_widget wpb_content_element"]/h2/text()').extract()
        for store in store_list:
            if self.validate(store.xpath('.//div[@class="wpb_column vc_column_container vc_col-sm-3"]')[0].xpath('.//p/strong/text()').extract_first()).find('Phone') == -1:
                return
            self.parse_store_content(store.xpath('.//div[@class="wpb_column vc_column_container vc_col-sm-3"]')[0], store.xpath('.//div[@class="wpb_column vc_column_container vc_col-sm-3"]')[1])
            if len(store.xpath('.//div[@class="wpb_column vc_column_container vc_col-sm-3"]')) == 4:
                if self.validate(store.xpath('.//div[@class="wpb_column vc_column_container vc_col-sm-3"]')[2].xpath('.//p/strong/text()').extract_first()).find('Phone') == -1:
                    return
                self.parse_store_content(store.xpath('.//div[@class="wpb_column vc_column_container vc_col-sm-3"]')[2], store.xpath('.//div[@class="wpb_column vc_column_container vc_col-sm-3"]')[3])


    def parse_store_content(self, address_content, hours_contents):
        pdb.set_trace()
        item = ChainItem()
        # address parsing
        _address = address_content.xpath('.//p//text()').extract()
        _address = [tp.strip().replace('\n', '') for tp in _address if tp.strip() != ""]
        address = []
        for x, val in enumerate(_address):
            if self.validate(val).find('Phone') != -1:
                item['phone_number'] = _address[x+1]
                break
            else:
                address.append(val)
                addr = usaddress.parse(" ".join(address))
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
        # hour parsing
        hours = hours_contents.xpath('.//p')
        item['store_hours'] = ''
        for hour in hours:
            item['store_hours'] += hour.xpath('.//strong/text()').extract_first() + hour.xpath('.//text()').extract()[1] + '; '

        item['store_number'] = ''
        item['country'] = 'United States'
        item['latitude'] = ''
        item['longitude'] = ''
        item['store_name'] = name_list[self.idx]
        item['other_fields'] = ""
        item['coming_soon'] = "0"

        self.idx += 1
        yield item

    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

