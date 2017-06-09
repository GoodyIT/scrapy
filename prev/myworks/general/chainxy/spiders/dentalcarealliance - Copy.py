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

class Dentalcarealliance(scrapy.Spider):
    name = "dentalcarealliance"

    domain = "http://www.dentalcarealliance.net/"
    start_urls = ["http://www.dentalcarealliance.net/"]
    store_id = []

    def parse(self, response):
        url_list = response.xpath('.//select[@name="header_state"]/option/@value').extract()
        for url in url_list:
            if url.strip() != '':
                if url[-1] == '/':
                    yield scrapy.Request(url="http://www.dentalcarealliance.net/affiliated-practices/" + url, callback=self.parse_second)
                else:
                    yield scrapy.Request(url="http://www.dentalcarealliance.net/affiliated-practices/" + url + '/', callback=self.parse_second)
             
    def parse_second(self, response):
        url_list = response.xpath('.//ul[@class="locations_list no_bullets"]/li/a/@href').extract()
        for url in url_list:
            # if url.find('virginia') != -1:
            #     pdb.set_trace()
            if url.strip() != '':
                if url[-1] == '/':
                    yield scrapy.Request(url=url, callback=self.parse_store)
                else:
                    yield scrapy.Request(url=url + '/', callback=self.parse_store)
     
    def parse_store(self, response):
        if response.url.find('http://smilesincluded.com/brooksville-dental-office/') != -1:
            pdb.set_trace()
        store_name = self.validate(response.xpath('.//div[@class="header_meta-line header_location-name"]/text()').extract_first())
        if store_name != '':
            pass
            try:
                item = ChainItem()
                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['store_name'] = self.validate(response.xpath('.//div[@class="header_meta-line header_location-name"]/text()').extract_first())
                item['address'] = self.validate(response.xpath('.//div[@class="header_meta-line header_location-address"]/span[1]/text()').extract_first())
                item['country'] = 'United States'
                item['city'] = self.validate(response.xpath('.//div[@class="header_meta-line header_location-address"]/span[2]/span[1]/text()').extract_first())
                item['state'] =  self.validate(response.xpath('.//div[@class="header_meta-line header_location-address"]/span[2]/span[2]/text()').extract_first())
                item['zip_code'] =  self.validate(response.xpath('.//div[@class="header_meta-line header_location-address"]/span[2]/span[3]/text()').extract_first())
                item['address2'] = ''
                item['phone_number'] = self.validate(response.xpath('.//div[@class="header_phone header_meta-line"]/a/text()').extract_first())
                hours = response.xpath('.//div[@class="office-information_section"]')[1].xpath('.//div[@class="office-information_item"]')
                item['store_hours'] = ''
                for hour in hours:
                    item['store_hours'] = hour.xpath('.//text()').extract_first() + hour.xpath('.//strong/text()').extract_first() + "; "

                yield item
            except:
                yield scrapy.Request(url=response.url, callback=self.parse_exception1, dont_filter=True)
        else:
            yield scrapy.Request(url=response.url, callback=self.parse_exception1, dont_filter=True)
            
    def parse_exception1(self, response):
        store_name = self.validate(response.xpath('.//div[@id="location_individual_info_address"]/h2/text()').extract_first())
        if store_name != '':
            try:
                item = ChainItem()
                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['address2'] = ''
                item['country'] = 'United States'
                item['store_name'] = self.validate(response.xpath('.//div[@id="location_individual_info_address"]/h2/text()').extract_first())
                item['address'] = response.xpath('.//span[@itemprop="streetAddress"]/text()').extract_first()
                item['city'] = response.xpath('.//span[@itemprop="addressLocality"]/text()').extract_first()
                item['state'] =  response.xpath('.//span[@itemprop="addressRegion"]/text()').extract_first()
                item['zip_code'] =  response.xpath('.//span[@itemprop="postalCode"]/text()').extract_first()
                item['phone_number'] = response.xpath('.//div[@class="location-full__phone"]/text()').extract_first()
                hours = response.xpath('.//div[@id="location_individual_info_hours"]/ul/li/text()').extract()
                item['store_hours'] = '; '.join(hours)

                yield item
            except:
                yield scrapy.Request(url=response.url, callback=self.parse_exception2, dont_filter=True)
        else:
            yield scrapy.Request(url=response.url, callback=self.parse_exception2, dont_filter=True)

    def parse_exception2(self, response):
        if response.url.find('http://smilesincluded.com/brooksville-dental-office/') != -1:
            pdb.set_trace()
        store_name = self.validate(response.xpath('.//div[@class="one_fourth last_column"]//div[@class="textwidget"]/p[1]/text()').extract_first())
        if store_name != '': 
            try:
                item = ChainItem()
                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['address2'] = ''
                item['country'] = 'United States'
                item['store_name'] = self.validate(response.xpath('.//div[@class="one_fourth last_column"]//div[@class="textwidget"]/p[1]/text()').extract_first())
                address = response.xpath('.//div[@class="one_fourth last_column"]//div[@class="textwidget"]/p[2]/text()').extract()
                address = [tp.strip().replace('\n', '') for tp in address if tp.strip() != ""]
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
                item['phone_number'] = self.validate(response.xpath('.//div[@class="one_fourth last_column"]//div[@class="textwidget"]/p[3]/text()').extract_first())
                hours = response.xpath('.//div[@class="office-information_section"]')[1].xpath('.//div[@class="office-information_item"]')
                item['store_hours'] = ''
                for hour in hours:
                    item['store_hours'] = hour.xpath('.//text()').extract_first() + hour.xpath('.//strong/text()').extract_first() + "; "
                yield item
            except:
                yield scrapy.Request(url=response.url, callback=self.parse_exception3, dont_filter=True)
        else:
            yield scrapy.Request(url=response.url, callback=self.parse_exception3, dont_filter=True)

    def parse_exception3(self, response):
        store_name = self.validate(response.xpath('.//div[@id="comp-logo"]/div[@id="logo"]/a/text()').extract_first())
        if store_name != '':
            try:
                item = ChainItem()
                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['address2'] = ''
                item['country'] = 'United States'
                item['store_name'] = self.validate(response.xpath('.//div[@id="comp-logo"]/div[@id="logo"]/a/text()').extract_first())
                address = response.xpath('.//div[@class="location-full__address"]/text()').extract()
                address = [tp.strip().replace('\n', '') for tp in address if tp.strip() != ""]
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
                item['phone_number'] = response.xpath('.//div[@class="location-full__phone"]/text()').extract_first()
                item['store_hours'] = ''

                yield item
            except:
                yield scrapy.Request(url=response.url, callback=self.parse_exception4, dont_filter=True)
        else:
            yield scrapy.Request(url=response.url, callback=self.parse_exception4, dont_filter=True)

    def parse_exception4(self, response):
        store_name = self.validate(response.xpath('.//div[@class="site-logo"]//img/@alt').extract_first())
        if store_name != '':
            try:
                item = ChainItem()
                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['address2'] = ''
                item['country'] = 'United States'
                item['store_name'] = self.validate(response.xpath('.//div[@class="site-logo"]//img/@alt').extract_first())
                address = self.validate(response.xpath('.//li[@id="menu-item-49"]/a/text()').extract_first())
                addr = usaddress.parse(address)
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
                item['phone_number'] = response.xpath('.//span[@class="tel"]/text()').extract_first()
                item['store_hours'] = ''

                yield item
            except:
                yield scrapy.Request(url=response.url, callback=self.parse_exception5, dont_filter=True)
        else:
            yield scrapy.Request(url=response.url, callback=self.parse_exception5, dont_filter=True)

    def parse_exception5(self, response):
        store_name = self.validate(response.xpath('.//article[@class="meta"]/p[2]/text()').extract_first())
        if store_name != '':
            try:
                item = ChainItem()
                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['address2'] = ''
                item['country'] = 'United States'
                item['store_name'] = self.validate(response.xpath('.//article[@class="meta"]/p[2]/text()').extract_first())
                address = self.validate(response.xpath('.//article[@class="meta"]/p[2]//text()').extract()[1])
                addr = usaddress.parse(address)
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
                item['phone_number'] = self.validate(response.xpath('.//article[@class="meta"]/p[1]/text()').extract_first())
                item['store_hours'] = ''
                yield item
            except:
                yield scrapy.Request(url=response.url, callback=self.parse_exception6, dont_filter=True)
        else:
            yield scrapy.Request(url=response.url, callback=self.parse_exception6, dont_filter=True)

    def parse_exception6(self, response):
        store_name = self.validate(response.xpath('.//div[@class="primary"]//img/@alt').extract_first())
        if store_name != '':
            try:
                item = ChainItem()
                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['address2'] = ''
                item['country'] = 'United States'
                item['store_name'] = self.validate(response.xpath('.//div[@class="primary"]//img/@alt').extract_first())
                address = response.xpath('.//div[@class="address"]//text()').extract()
                address = [tp.strip().replace('\n', '') for tp in address if tp.strip() != ""]
                addr = usaddress.parse(address)
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
                item['phone_number'] = self.validate(response.xpath('.//span[@class="phoneNumber"]/a/text()').extract_first())
                item['store_hours'] = ''
                yield item
            except:
                yield scrapy.Request(url=response.url, callback=self.parse_exception7, dont_filter=True)
        else:
            yield scrapy.Request(url=response.url, callback=self.parse_exception7, dont_filter=True)

    def parse_exception7(self, response):
        store_name = self.validate(response.xpath('.//td[@class="practicename"]//text()').extract_first())
        if store_name != '':
            try:
                item = ChainItem()
                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['address2'] = ''
                item['country'] = 'United States'
                item['store_name'] = store_name
                address = response.xpath('.//div[@class="address"]//text()').extract()
                address = [tp.strip().replace('\n', '') for tp in address if tp.strip() != ""]
                addr = usaddress.parse(address)
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
                item['phone_number'] = self.validate(response.xpath('.//span[@class="phoneNumber"]/a/text()').extract_first())
                item['store_hours'] = ''
                yield item
            except:
                yield scrapy.Request(url=response.url, callback=self.parse_exception8, dont_filter=True)
        else:
            yield scrapy.Request(url=response.url, callback=self.parse_exception8, dont_filter=True)

    def parse_exception8(self, response):
        store_name = self.validate(response.xpath('.//div[@id="logo"]//img/@alt').extract_first())
        if store_name != '':
            try:
                item = ChainItem()
                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['address2'] = ''
                item['country'] = 'United States'
                item['store_name'] = store_name
                address = response.xpath('.//div[@id="googlemapswidget-2"]/p[2]/text()').extract()
                address = [tp.strip().replace('\n', '') for tp in address if tp.strip() != ""]
                addr = usaddress.parse(address)
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
                item['phone_number'] = ''
                item['store_hours'] = "; ".join(response.xpath('.//div[@class="footer-sidebar-1 widget-area col-sm-4"]/div[1]//text()').extract())
                yield item
            except:
                if response.url.find('smilesatfairfaxcorner') != -1:
                    yield scrapy.Request(url=response.url, callback=self.parse_exception9, dont_filter=True)
                else:
                    yield scrapy.Request(url=response.url, callback=self.parse_exception10, dont_filter=True)

        else:
            if response.url.find('smilesatfairfaxcorner') != -1:
                yield scrapy.Request(url=response.url, callback=self.parse_exception9, dont_filter=True)
            else:
                yield scrapy.Request(url=response.url, callback=self.parse_exception10, dont_filter=True)
    
    def parse_exception9(self, response):
        store_name = response.url.split('.')
        if store_name != '':
            try:
                item = ChainItem()
                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                item['other_fields'] = ""
                item['coming_soon'] = "0"
                item['address2'] = ''
                item['country'] = 'United States'
                item['store_name'] = store_name
                address = response.xpath('.//div[@id="googlemapswidget-2"]/p[2]/text()').extract()
                address = [tp.strip().replace('\n', '') for tp in address if tp.strip() != ""]
                addr = usaddress.parse(address)
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
                item['phone_number'] = ''
                item['store_hours'] = "; ".join(response.xpath('.//div[@class="footer-sidebar-1 widget-area col-sm-4"]/div[1]//text()').extract())
                yield item
            except:
                pdb.set_trace()
        else:
            pdb.set_trace()

    def parse_exception10(self, response):
        pdb.set_trace()

    def validate(self, value):
        if value != None:
            return value.replace(u'\u2019', '-').replace(u'\u2013', '-').replace('Phone:', '').strip()
        else:
            return ""





        

