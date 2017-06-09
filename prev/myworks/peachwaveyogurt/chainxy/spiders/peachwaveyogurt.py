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

class Peachwaveyogurt(scrapy.Spider):
    name = "peachwaveyogurt"

    domain = "http://www.peachwaveyogurt.com/"
    start_urls = ["http://www.peachwaveyogurt.com/locations/?q=&search=Search"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//div[@class="cms-loc-directory-view-details"]/a/@href').extract()
        for store in store_list:
            yield scrapy.Request(url=store, callback=self.parse_store)

    def parse_store(self, response):
        item = ChainItem()

        item['store_number'] = ''
        item['store_name'] = response.xpath('//div[@class="page-title-wrap"]/h1/text()').extract_first()
        address = response.xpath('.//div[@class="address"]/p/text()').extract()
        if len(address) == 0:
            address = response.xpath('.//div[@class="address"]/p/span/text()').extract()

        item['country'] = 'United States'
        item['phone_number'] = response.xpath('.//div[@class="phone"]/p/text()').extract_first()
        item['latitude'] = response.xpath('.//script/text()').extract()[3].split('new google.maps.LatLng(')[1].strip().split(');\n\tvar')[0].strip().split(',')[0]
        item['longitude'] = response.xpath('.//script/text()').extract()[3].split('new google.maps.LatLng(')[1].strip().split(');\n\tvar')[0].strip().split(',')[1]
       
        item['other_fields'] = ""
        item['address2'] = ''
        if len(address) != 0:
            item['address'] = address[0].strip()
            address1 = ''
            if len(address) == 3:
                item['address2'] = address[1].strip()
                address1 = address[2]
            elif len(address) == 2:
                address1 = address[1]
            else:
                return
            if len(address1.split(',')) > 2:
                if address1.find('Cayman Islands') != -1:
                    item['address2'] = address1.split(',')[0]
                    item['city'] = address1.split(',')[1]
                    item['state'] = ''
                    item['zip_code'] = ''
                    item['country'] = address1.split(',')[2]
                else:
                    return
            else:
                if address1.find(',') != -1:
                    item['city'] = address1.split(',')[0].strip()
                    spliter = ' '
                    address1 = address1.encode('utf8').replace('\xc2\xa0', '').strip()
                    if address1.find(';') != -1:
                        item['state'] = address1.split(',')[1].strip().split(';')[0].strip()
                        item['zip_code'] = address1.split(',')[1].strip().split(';')[1].strip()
                    elif address1.find('\xc2\xa0') != -1:    
                        item['state'] = address1.split(',')[1].strip().split('\xc2\xa0')[0].strip()
                        item['zip_code'] = address1.split(',')[1].strip().split('\xc2\xa0')[1].strip()
                    else:
                        item['state'] = address1.split(',')[1].strip().split(' ')[0].strip()
                        item['zip_code'] = address1.split(',')[1].strip().split(' ')[1].strip()
                else:
                    item['city'] = address1.split(' ')[0].strip()
                    item['state'] = address1.split(' ')[1].strip()
                    item['zip_code'] = address1.split(' ')[2].strip()

            hours = response.xpath('.//div[@class="cms-loc-directory-hours"]/ul/li')
            item['store_hours'] = ''
            if len(hours) == 0:
                hours = response.xpath('.//div[@class="cms-loc-directory-part-hours"]/p')
            if len(hours) != 0:
                if hours.xpath('.//text()').extract_first().find('Coming Soon') != -1:
                    item['coming_soon'] = "1"
                    yield item
                for hour in hours:
                    item['store_hours'] +=  hour.xpath('.//text()').extract()[0] + hour.xpath('.//text()').extract()[1] + "; "
                
            item['coming_soon'] = "0"
        else:
            item['address'] = ''
            item['city'] = ''     
            item['state'] = ''
            item['zip_code'] = ''
            item['coming_soon'] = "1"
        
        if item['state'].find('BC') != -1:
            item['country'] = 'Canada'
        yield item




        

