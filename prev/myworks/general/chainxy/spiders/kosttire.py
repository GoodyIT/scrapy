import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem

import pdb
from scrapy.http import HtmlResponse
from lxml import html
from lxml.html import fromstring
import geocoder

class Kosttire(scrapy.Spider):
    name = "kosttire"

    domain = "http://www.mrtire.com/"
    start_urls = ["http://locations.mrtire.com/"]
    directory_url = "http://locations.mrtire.com/%s"

    # calculate number of pages
    def parse(self, response):
        directory_list = response.xpath('//ul[@class="c-directory-list-content"]/li[@class="c-directory-list-content-item"]/a[@class="c-directory-list-content-item-link"]/@href').extract()
        
        for link in directory_list:
            if len(link.split('/')) > 1:
                yield scrapy.Request(url=self.directory_url % link.replace('../', ''), callback=self.parse_store)
            else:
                yield scrapy.Request(url=self.directory_url % link.replace('../', ''), callback=self.parse)
     
    # pare store detail page
    def parse_store(self, response):
        # if response.url.find('http://locations.mrtire.com/va/springfield/6413-backlick-road.html') != -1:
        #     pdb.set_trace()
        store_list = response.xpath('.//div[@class="row c-location-grid-row"]')
        if len(store_list) == 0:
            store = response
            item = ChainItem()
            item['store_number'] = ''
            
            item['store_name'] = store.xpath(".//span[contains(@class, 'location-name-name')]/text()").extract_first()
            item['latitude'] = ''
            item['longitude'] = ''
            item['city'] = store.xpath(".//span[contains(@class, 'c-address-city')]/span/text()").extract_first()
            item['state'] = store.xpath(".//span[contains(@class, 'c-address-state')]/text()").extract_first()
            item['zip_code'] = store.xpath(".//span[contains(@class, 'c-address-postal-code')]/text()").extract_first()
            item['country'] = 'United States'
            item['address'] = store.xpath(".//span[contains(@class, 'c-address-street c-address-street-1')]/text()").extract_first()
            try:
                item['address2'] = store.xpath(".//span[contains(@class, 'c-address-street-2')]/text()").extract_first()
            except:
                item['address2'] = ''

            item['phone_number'] = store.xpath(".//span[@class='c-phone-number-span c-phone-main-number-span']/text()").extract_first()

            hour_list = []
            try:
                hours = store.xpath('.//table[@class="c-location-hours-details"]//tr')
                for hour in hours:
                    day = hour.xpath('.//td[@class="c-location-hours-details-row-day"]/text()').extract_first()
                    hour_list.append(day + ' ' + hour.xpath('.//span[@class="c-location-hours-details-row-intervals-instance-open"]/text()').extract_first() + ' - ' + hour.xpath('.//span[@class="c-location-hours-details-row-intervals-instance-close"]/text()').extract_first())

                item['store_hours'] = "; ".join(hour_list)
            except:
                item['store_hours'] = ''
            
            item['other_fields'] = ''
            item['coming_soon'] = '0'
            
            yield item
        else:
            for store in store_list:
                item = ChainItem()
                item['store_number'] = ''
                
                item['store_name'] = store.xpath(".//span[contains(@class, 'location-name-name')]/text()").extract_first()
                item['latitude'] = ''
                item['longitude'] = ''
                item['city'] = store.xpath(".//span[contains(@class, 'c-address-city')]/span/text()").extract_first()
                item['state'] = store.xpath(".//span[contains(@class, 'c-address-state')]/text()").extract_first()
                item['zip_code'] = store.xpath(".//span[contains(@class, 'c-address-postal-code')]/text()").extract_first()
                item['country'] = 'United States'
                item['address'] = store.xpath(".//span[contains(@class, 'c-address-street c-address-street-1')]/text()").extract_first()
                try:
                    item['address2'] = store.xpath(".//span[contains(@class, 'c-address-street-2')]/text()").extract_first()
                except:
                    item['address2'] = ''

                item['phone_number'] = store.xpath(".//span[@class='c-phone-number-span c-phone-main-number-span']/text()").extract_first()

                hour_list = []
                item['store_hours'] = ''
                
                item['other_fields'] = ''
                item['coming_soon'] = '0'
                
                yield item

    def validate(self, store, property):
        if property in store:
            return store[property]
        return ""

    def remove_prefix(self, text, prefix):
        return text.replace("../", "")  # or whatever


        

