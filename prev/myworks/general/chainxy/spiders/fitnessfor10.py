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

class Fitnessfor10(scrapy.Spider):
    name = "fitnessfor10"

    domain = "http://www.fitnessfor10.com"
    start_urls = ["http://fitnessfor10.com/locations/"]
    store_id = []

    def parse(self, response):
        store_list = response.xpath('.//div[@class="wpb_wrapper"]/div[contains(@class,"info-box")]/a/@href').extract()
        for store in store_list:
            yield scrapy.Request(url= store[:-1], callback=self.parse_store_second)

    def parse_store_second(self, response):
        store_list = response.xpath('.//div[@class="wpb_wrapper"]/div[contains(@class,"info-box")]/a/@href').extract()
        for store in store_list:
            yield scrapy.Request(url= store[:-1], callback=self.parse_store)

    def parse_store(self, response):
        try:
            item = ChainItem()
            item['store_number'] = ''
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_name'] = response.xpath('.//div[@class="vc_separator wpb_content_element vc_separator_align_center vc_sep_width_100 vc_sep_pos_align_center vc_separator-has-text"]/h4/text()').extract_first().replace('Fitness For 10 -', '')

            item['other_fields'] = ""
            item['coming_soon'] = "0"
            address = response.xpath('.//div[@class="vc_row wpb_row vc_row-fluid"]//div[@class="wpb_text_column wpb_content_element "]')[0].xpath('.//div[1]//h3/text()').extract()
            address = [tp.strip().replace('\n', '') for tp in address if tp.strip() != ""]
            item['address'] = address[0]
            item['address2'] = ''
            loc = 0
            ca = 0
            for x, addr in enumerate(address):
                if addr.lower().find('(306)') != -1:
                    ca = x - 1
                if addr.lower().find('ph:') != -1:
                    loc = x -1
                    break

            if ca != 0:
                item['country'] = 'Canada'
                if address[loc].find(',') != -1:
                    item['city'] = address[loc].split(',')[1]
                    item['address'] = address[loc].split(',')[0].replace(',', '')
                    item['state'] = address[loc].split(',')[1].strip().split(' ')[0]
                    item['zip_code'] = " ".join(address[loc].split(',')[1].strip().split(' ')[1:])
                else:
                    if len(address[loc].split(' ')) == 4:
                        item['city'] = address[loc-1].split(',')[1]
                        item['state'] = address[loc].split(' ')[0].strip()
                        item['zip_code'] = " ".join(address[loc].split(' ')[1:])
                    else:
                        item['city'] = ''
                        item['state'] = ''
                        item['zip_code'] = address[loc]
            else:
                item['city'] = address[loc].split(',')[0]
                item['state'] = address[loc].split(',')[1].strip().split(' ')[0]
                item['zip_code'] = " ".join(address[loc].split(',')[1].strip().split(' ')[1:])
                item['country'] = 'United States'
                   
            # if item['store_name'].find('Regina, Saskatchewan') != -1:
            #     pdb.set_trace()
            item['phone_number'] =  address[loc+1].replace('Ph:', '').replace('PH:', '').strip()

            hours = response.xpath('.//div[@class="wpb_text_column wpb_content_element "]')[1].xpath('.//div[1]//h3/text()').extract()
            hours = [tp.strip().replace('\n', '').replace(u'\u2013', '-') for tp in hours if tp.strip() != ""]
            item['store_hours'] = "; ".join(hours).replace('*Temporary Staffed Hours*;', '').replace('AVAILABLE TO MEMBERS 24/7!; Regular Staffed Hours:;', '').replace('AVAILABLE TO VIP/VIP+ MEMBERS 24/7!; Regular Staffed Hours:;', '').replace('*Current Staffed Hours*;', '').replace('AVAILABLE TO MEMBERS 24/7!; Regular Staffed Hours:;', '').replace('Staffed Hours;', '').strip()
      
            yield item
        except:
            pdb.set_trace()
    
    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

