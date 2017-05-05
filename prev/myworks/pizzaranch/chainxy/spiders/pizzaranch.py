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

class Pizzaranch(scrapy.Spider):
    name = "pizzaranch"

    domain = "http://www.pizzaranch.com//"
    start_urls = ["http://www.pizzaranch.com/locations/"]
    directory_url = "http://www.pizzaranch.com/locations/%s"

    def __init__(self):

        self.store_numbers = []

    # calculate number of pages
    def parse(self, response):
        directory_list = response.xpath('//ul[@class="c-directory-list-content"]/li[@class="c-directory-list-content-item"]')
        if (directory_list != []):

            for directory in directory_list:
                link = self.directory_url % directory.xpath('./a[@class="c-directory-list-content-item-link"]/@href').extract_first()
                item_count = int(directory.xpath('.//span/text()').extract_first())

                if item_count == 1:
                    request = scrapy.Request(url=self.remove_prefix(link, '../'), callback=self.parse_store)
                else:
                    request = scrapy.Request(url=link, callback=self.parse)

                yield request
        else:
            directory_list = response.xpath('//*[@id="main"]/div[3]/div/div[1]')

            for directory in directory_list:
                link = self.directory_url % directory.xpath('.//div/h3/a/@href').extract_first()
                request = scrapy.Request(url=self.remove_prefix(link, '../'), callback=self.parse_store)

                yield request
     
    # pare store detail page
    def parse_store(self, response):
        left_content = response.xpath('//div[@class="content-wrapper"]')[0]

        item = ChainItem()
        item['store_number'] = ''
        
        item['store_name'] = response.xpath(".//span[contains(@class, 'location-name-brand')]/text()").extract_first() + ' ' + response.xpath(".//span[contains(@class, 'location-name-geo')]/text()").extract_first()
        geo = left_content.xpath('.//*[@id="location-info-left"]/div/div[2]/div[2]/div/div[3]/span/meta')
        item['latitude'] = response.xpath('.//*[@id="location-info-left"]/div/div[2]/div[2]/div/div[3]/span/meta[1]/@content').extract_first()
        item['longitude'] = response.xpath('.//*[@id="location-info-left"]/div/div[2]/div[2]/div/div[3]/span/meta[2]/@content').extract_first()
        item['city'] = left_content.xpath(".//span[contains(@class, 'c-address-city')]/span[1]/text()").extract_first()
        item['state'] = left_content.xpath(".//abbr[contains(@class, 'c-address-state')]/text()").extract_first()
        item['zip_code'] = left_content.xpath(".//span[contains(@class, 'c-address-postal-code')]/text()").extract_first()
        item['country'] = 'United States'
        item['address'] = left_content.xpath(".//span[contains(@class, 'c-address-street-1')]/text()").extract_first()

        try:
            item['address2'] = left_content.xpath('.//span[@class="c-address-street"]/span[@class="c-address-street-2"]/text()').extract_first()
        except:
            item['address2'] = ''

        item['phone_number'] = left_content.xpath(".//span[@id='telephone']/text()").extract_first()

        hour_list = []
        try:
            hours = response.xpath('.//*[@id="location-info-right"]/div/div[1]/div/div/table/tbody/tr')
            for hour in hours:
                day = hour.xpath('.//td[@class="c-location-hours-details-row-day"]/text()').extract_first()
                time = hour.xpath('.//td[@class="c-location-hours-details-row-intervals"]/span')[0]
                hour_list.append(day + ' ' + time.xpath('.//span[@class="c-location-hours-details-row-intervals-instance-open"]/text()').extract_first() + ' - ' + time.xpath('.//span[@class="c-location-hours-details-row-intervals-instance-close"]/text()').extract_first())

            item['store_hours'] = "; ".join(hour_list)
        except:
            item['store_hours'] = ''
        
        #item['store_type'] = info_json["@type"]
        item['other_fields'] = ''
        item['coming_soon'] = '0'
        
        yield item

    def validate(self, store, property):
        if property in store:
            return store[property]
        return ""

    def remove_prefix(self, text, prefix):
        return text.replace("../", "")  # or whatever


        

