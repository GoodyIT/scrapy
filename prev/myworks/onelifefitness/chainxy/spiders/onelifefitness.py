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

class Onelifefitness(scrapy.Spider):
    name = "onelifefitness"

    domain = "https://www.onelifefitness.com/"
    start_urls = ["https://www.onelifefitness.com"]
    store_id = []

    def parse(self, response):
        parents = response.xpath('.//div[@id="hs_menu_wrapper_module_14652775546295339"]//ul/li[2]')
        for parent in parents:
            if parent.xpath('.//a/text()').extract_first().find('Locations') != -1:
                branch_list = parent.xpath('.//ul[contains(@class, "hs-menu-children-wrapper")]/li/a/@href').extract()
                for branch in branch_list:
                    branch = branch.replace('https://www.onelifefitness.com', '')
                    if branch.find('onelifekc') == -1:
                        request = scrapy.Request(url="https://www.onelifefitness.com%s" % branch, callback=self.parse_clubs)
                    else:
                        request = scrapy.Request(url=branch, callback=self.parse_kensas)
                    yield request
    def parse_kensas(self, response):
        item = ChainItem()
        item['store_number'] = ''
        item['coming_soon'] = "0"
        item['store_name'] = response.xpath('.//a[@class="standard-logo"]/img/@alt').extract_first()
        address = response.xpath('.//address/a[1]/text()').extract()
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
        item['country'] = 'United States'
        item['city'] = city
        item['state'] =  state
        item['zip_code'] =  zip_code
        item['phone_number'] = response.xpath('.//address/a/text()').extract_first()
        item['latitude'] = ''
        item['longitude'] = ''
        item['store_hours'] = ""
        item['other_fields'] = ""   

        yield item

    def parse_clubs(self, response):
        club_list = response.xpath('.//ul[contains(@class, "gym_locations")]/li')
        for club in club_list:
            request = scrapy.Request(url="https://www.onelifefitness.com%s" % club.xpath('.//a/@href').extract_first(), callback=self.parse_store)
            request.meta['lat'] = club.xpath('.//@data-lat').extract_first()
            request.meta['lng'] = club.xpath('.//@data-ln').extract_first()
            yield request

    def parse_store(self, response):
        # try:
        item = ChainItem()

        item['store_number'] = ''
        item['store_name'] = response.xpath('.//div[@class="banner-header"]/h1/text()').extract_first()
        item['address'] = response.xpath('.//span[@id="hs_cos_wrapper_module_14684752951104419"]/p/span[1]/text()').extract_first()
        address = ''
        # if item['store_name'].find('Windermere Gym') != -1:
        #     pdb.set_trace()
        if item['address'] == None:
            item['address'] = response.xpath('.//span[@id="hs_cos_wrapper_module_14684752951104419"]/p[1]/text()').extract_first()
            if item['address'] == None:
                item['address'] = response.xpath('.//span[@id="hs_cos_wrapper_module_14684752951104419"]/text()').extract_first()
                address = response.xpath('.//span[@id="hs_cos_wrapper_module_14684752951104419"]/text()').extract()[1]
            else:
                address = response.xpath('.//span[@id="hs_cos_wrapper_module_14684752951104419"]/p/text()').extract()[1]
        else:
            address = response.xpath('.//span[@id="hs_cos_wrapper_module_14684752951104419"]/p/span[2]/text()').extract_first()
        
        if len(address.split(',')) == 2:
            item['city'] = address.split(',')[0].strip()
            item['state'] = address.split(',')[1].strip().split(' ')[0].strip()
            item['zip_code'] = address.split(',')[1].strip().split(' ')[1].strip()
        elif len(address.split(',')) == 3:
            item['city'] = address.split(',')[0].strip()
            item['state'] = address.split(',')[1].strip()
            item['zip_code'] = address.split(',')[2].strip()
        else:
            item['city'] = address.split(' ')[0].strip()
            item['state'] = address.split(' ')[1].strip()
            item['zip_code'] = address.split(' ')[2].strip()
        
        item['address2'] = ''
        item['country'] = 'United States'
        item['coming_soon'] = "0"
        item['latitude'] = response.meta['lat']
        item['longitude'] = response.meta['lng']
        item['other_fields'] = ""   

        phone = response.xpath('.//span[@id="hs_cos_wrapper_module_14684754122179512"]/p/text()').extract_first()
        if phone == None:
            phone = response.xpath('.//span[@id="hs_cos_wrapper_module_14684754122179512"]/p/a/text()').extract_first()
      
        if phone == None:
            item['phone_number'] = ''
        elif phone.find('Coming Soon') == -1:
            item['phone_number'] = self.validate(phone)
        else:
            item['coming_soon'] = "1"
        
        item['store_hours'] = ""
        

        hours = response.xpath('.//span[@id="hs_cos_wrapper_module_14684754134419869"]/p/text()').extract_first()
        if hours != None and hours.find('Coming Soon') != -1:
            item['coming_soon'] = "1"
        else:
            try:
                item['store_hours'] = "; ".join(response.xpath('.//span[@id="hs_cos_wrapper_module_14684754134419869"]/p/text()').extract()).strip()
                item['store_hours'] = item['store_hours'][2:].strip()
            except:
                item['store_hours'] = ""

        # if item['store_name'].find('Crabapple Gym') != -1:
        #     pdb.set_trace()
        item['store_hours'] = self.validate(item['store_hours'])
        # except:
        #     pdb.set_trace()
        yield item

    def validate(self, value):
        return value.encode('utf8').replace('\xc2\xa0', ' ')




        

