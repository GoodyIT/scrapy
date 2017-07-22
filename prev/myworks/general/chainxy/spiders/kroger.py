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
from lxml import etree
from selenium import webdriver
import time

class Kroger(scrapy.Spider):
    name = "kroger"

    domain = "https://www.kroger.com"
    start_urls = ["https://www.kroger.com/stores/search?searchText=60004"]
    store_name = []

    def __init__(self):
        self.driver = webdriver.Chrome("./chromedriver")

    def start_requests(self):
        yield scrapy.Request(url="http://biscuitscafe.com/", callback=self.parse_store)

    def parse_store(self, response):
        source_list = []
        for x in range(1, 14):
            url = "https://www.kroger.com/stores/search?searchText=Houston&selectedPage="+str(x)
            self.driver.get(url)
            time.sleep(1)
            source = self.driver.page_source.encode("utf8")
            tree = etree.HTML(source)
            url_list = tree.xpath('.//div[@class="StoreResult"]//a[@class="StoreResult-viewDetailsLink Link"]/@href')
            for url in url_list:
                self.driver.get("https://www.kroger.com"+url)
                time.sleep(1)
                source = self.driver.page_source.encode("utf8")
                store = etree.HTML(source)
                item = ChainItem()
                item['store_number'] = ''
                item['country'] = 'United States'
                item['latitude'] = ''
                item['longitude'] = ''
                try:
                    item['store_name'] = store.xpath('.//div[@class="StoreInformation-storeName"]/text()')[0]
                except:
                    item['store_name'] = ''

                if item['store_name'] in self.store_name:
                    continue
                self.store_name.append(item['store_name'])

                item['other_fields'] = ""
                item['coming_soon'] = "0"
                address = store.xpath('.//div[@class="StoreAddress-storeAddressGuts"]/text()')
                address = [tp.strip().replace('\n', '') for tp in address if tp.strip() != ""]
                item['address'] = address[0]
                item['address2'] =  ''
                item['city'] = address[1]
                item['state'] =  address[3]
                item['zip_code'] = address[4]
                item['phone_number'] =  store.xpath('.//span[@class="PhoneNumber-phone"]/text()')[0]
                
                hours = store.xpath('.//table[@class="StoreInformation-table"]//tr')
                item['store_hours'] = ''
                for hour in hours:
                    day = hour.xpath('.//td[1]/text()') 
                    day = [tp.strip().replace('\n', '') for tp in day if tp.strip() != ""]
                    item['store_hours'] += ''.join(day) + hour.xpath('.//td[2]/text()')[0] + '; '
                
                yield item

    def validate(self, value):
        if value != None:
            return value.strip().replace(u'\u2019', '-')
        else:
            return ""





        

