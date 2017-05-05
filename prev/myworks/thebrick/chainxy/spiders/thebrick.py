import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem

import pdb

class Thebrick(scrapy.Spider):
    name = "thebrick"

    domain = "https://www.thebrick.com/"
    start_urls = ["https://www.thebrick.com/store/locator/show-all-locations"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_list=response.xpath('.//*[@id="page-content"]/div/section/div[6]/div/div/div');
        for store_info in store_list:
            
            item = ChainItem()
            item['store_number'] = ''
            try:
                item['store_name'] = store_info.xpath(".//div[@data-store-name]/span/strong/text()").extract_first().split('-')[1].strip()
            except:
                item['store_name'] = ''
            item['address'] = store_info.xpath('.//span[@class="sl-address"]/span[@itemprop="streetAddress"]/text()').extract_first()
            item['city'] = store_info.xpath('.//span[@class="sl-address"]/span[@itemprop="addressLocality"]/text()').extract_first()
            item['state'] = store_info.xpath('.//span[@class="sl-address"]/span[@itemprop="addressRegion"]/text()').extract_first()
            item['zip_code'] = store_info.xpath('.//span[@class="sl-address"]/span[@itemprop="postalCode"]/text()').extract_first()
            item['phone_number'] = store_info.xpath('.//span[@class="sl-address"]/span/span[@itemprop="telephone"]/text()').extract_first()
            if item['zip_code'] == None:
                continue
            try:
                int(item['zip_code'])
                item['country'] = 'United States'
            except:
                item['country'] = "Canada"

            item['address2'] = ''
            item['latitude'] = ''
            item['longitude'] = ''
            hours = store_info.xpath('.//div/div/ul')
            hour_list = []
            for hour in hours:
                hour_list.append(hour.xpath('.//li/text()')[0].extract() + hour.xpath('.//li/text()')[1].extract())

            item['store_hours'] = ";".join(hour_list)
            item['other_fields'] = ""
            item['coming_soon'] = "0"
            
            yield item


        

