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

class Fareway(scrapy.Spider):
    name = "fareway"

    domain = "http://www.fareway.com/"
    start_urls = ["https://www.fareway.com/stores"]
    store_id = []

    def start_requests(self):
        for x in xrange(1,16):
            yield scrapy.Request(url='https://www.fareway.com/stores/page/%s'
                       % x, callback=self.parse_store)
    # calculate number of pages
    def parse_store(self, response):
        store_list = response.xpath('//div[@class="card store"]')
        for store_info in store_list:
            item = ChainItem()

            item['store_number'] = store_info.xpath('.//div[@class="card-content"]/h3/a/text()').extract_first().replace('#', '')
            item['store_name'] = store_info.xpath('.//div[@class="card-content"]/h3[@class="card-title"]/a/text()').extract()[1]
            item['address2'] = ''
            address = store_info.xpath('.//div[@class="card-content"]/p[@class="card-subtitle"]/text()').extract_first()
            item['address'] = "".join(address.split(',')[:-2]).strip()
            item['city'] = address.split(',')[-2].strip()
            item['state'] = address.split(',')[-1].strip().split(' ')[0]
            item['zip_code'] = address.split(',')[-1].strip().split(' ')[1]
                
            item['country'] = 'United States'
            item['phone_number'] = store_info.xpath('.//div[@class="card-content"]/div[@class="store-card-info"]/div[@class="store-phone"]/p[1]/span/text()').extract_first()
            item['latitude'] = store_info.xpath('.//@data-latitude').extract_first()
            item['longitude'] = store_info.xpath('.//@data-longitude').extract_first()

            hours = store_info.xpath('.//div[@class="card-content"]/div[@class="store-card-info"]/div[@class="store-hours"]//text()').extract() 
            hours = [tp.strip().replace('\n', '') for tp in hours if tp.strip() != ""]
            item['store_hours'] = "; ".join(hours)
            item['other_fields'] = ""
            item['coming_soon'] = "0"
                
            yield item





        

