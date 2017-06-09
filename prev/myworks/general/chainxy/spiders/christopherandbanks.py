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

class Christopherandbanks(scrapy.Spider):
    name = "christopherandbanks"

    domain = "https://stores.christopherandbanks.com"
    start_urls = ["https://stores.christopherandbanks.com/index.html"]
    directory_url = "https://stores.christopherandbanks.com/%s"

    def __init__(self):

        self.store_numbers = []

    # calculate number of pages
    def parse(self, response):
        directory_list = response.xpath('//ul[@class="c-directory-list-content"]/li[@class="c-directory-list-content-item"]')
        
        if (directory_list != []):
            for directory in directory_list:
                link = self.directory_url % directory.xpath('./a[@class="c-directory-list-content-item-link"]/@href').extract_first()
                item_count = int(directory.xpath('.//span/text()').extract_first()[1:-1])

                if item_count == 1:
                    request = scrapy.Request(url=link.replace('../', ''), callback=self.parse_store)
                else:
                    request = scrapy.Request(url=link, callback=self.parse)

                yield request
        else:
            directory_list = response.xpath('//div[@class="c-location-grid-col col-lg-3 col-sm-4 col-xs-12"]/div/h5/a/@href').extract()

            for directory in directory_list:
                link = self.directory_url % directory.replace('../', '')
                request = scrapy.Request(url=link, callback=self.parse_store)

                yield request
     
    # pare store detail page
    def parse_store(self, response):
        try:
            item = ChainItem()
            item['store_number'] = ''
            
            item['store_name'] = response.xpath(".//span[contains(@class, 'bottom-name')]/text()").extract_first()
            item['latitude'] = ''
            item['longitude'] = ''
            item['city'] = response.xpath(".//span[contains(@itemprop, 'addressLocality')]/text()").extract_first()
            item['state'] = response.xpath(".//abbr[contains(@class, 'c-address-state')]/text()").extract_first()
            item['zip_code'] = response.xpath(".//span[contains(@class, 'c-address-postal-code')]/text()").extract_first()
            item['country'] = 'United States'
            item['address'] = response.xpath(".//span[contains(@class, 'c-address-street-1')]/text()").extract_first()
            try:
                item['address2'] = response.xpath(".//span[contains(@class, 'c-address-street-2')]/text()").extract_first()
            except:
                item['address2'] = ''

            item['phone_number'] = response.xpath(".//span[@id='telephone']/text()").extract_first()

            hour_list = []
            try:
                hours = response.xpath('.//tr[@class="c-location-hours-details-row js-day-of-week-row  "]')
                for hour in hours:
                    day = hour.xpath('.//td[@class="c-location-hours-details-row-day"]/text()').extract_first()
                    time = hour.xpath('.//td[@class="c-location-hours-details-row-intervals"]/span')[0]
                    hour_list.append(day + ' ' + time.xpath('.//span[@class="c-location-hours-details-row-intervals-instance-open"]/text()').extract_first() + ' - ' + time.xpath('.//span[@class="c-location-hours-details-row-intervals-instance-close"]/text()').extract_first())

                item['store_hours'] = "; ".join(hour_list)
            except:
                item['store_hours'] = ''
            
            item['other_fields'] = ''
            item['coming_soon'] = '0'
            
            yield item
        except:
            pdb.set_trace()

    def validate(self, store, property):
        if property in store:
            return store[property]
        return ""

    def remove_prefix(self, text, prefix):
        return text.replace("../", "")  # or whatever


        

