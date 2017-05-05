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

class Sonicdrivein(scrapy.Spider):
    name = "sonicdrivein"

    domain = "http://en.store.dior.com/"
    start_urls = ["https://locations.sonicdrivein.com/index.html"]
    directory_url = "https://locations.sonicdrivein.com/%s"

    def __init__(self):

        self.store_numbers = []

    # calculate number of pages
    def parse(self, response):
        directory_list = response.xpath('//ul[@class="c-directory-list-content"]/li[@class="c-directory-list-content-item"]')

        if (directory_list != []):

            for directory in directory_list:
                link = self.directory_url % directory.xpath('./a[@class="c-directory-list-content-item-link"]/@href').extract_first()
                item_count = int(directory.xpath('./span/text()').extract_first())



                if item_count == 1:
                    request = scrapy.Request(url=self.remove_prefix(link, '../'), callback=self.parse_store)
                else:
                    request = scrapy.Request(url=link, callback=self.parse)

                yield request
        else:
            directory_list = response.xpath('//div[@class="c-location-grid"]/div[contains(@class, "c-location-grid-col")]')

            for directory in directory_list:
                link = self.directory_url % directory.xpath('./div/h3/a/@href').extract_first()
                request = scrapy.Request(url=self.remove_prefix(link, '../'), callback=self.parse_store)

                yield request
     
    # pare store detail page
    def parse_store(self, response):
        pdb.set_trace()
        left_content = response.xpath('//div[@class="nap-content-col-white-left"]')

        item = ChainItem();
        item['store_number'] = ''
        
        item['store_name'] = response.xpath('//h1[@class="nap-content-title"]/span[@class="location-name-geo"]/text()').extract_first()
        geo = left_content.xpath('//div[@class="nap-content-address"]/span[@class="coordinates"]/meta')
        item['latitude'] = geo[0].xpath('@content').extract_first()
        item['longitude'] = geo[1].xpath('@content').extract_first()
        address = left_content.xpath('//div[@class="nap-content-address"]/address[@class="c-address"]')
        item['address'] = address.xpath('//span[@class="c-address-street"]/span[@class="c-address-street-1"]/text()').extract_first()
        try:
            item['address2'] = address.xpath('//span[@class="c-address-street"]/span[@class="c-address-street-2"]/text()').extract_first()
        except:
            item['address2'] = ''

        item['city'] = address.xpath('//span[@class="c-address-city"]/span[@itemprop="addressLocality"]/text()').extract_first()
        item['state'] = address.xpath('//abbr[@class="c-address-state"]/text()').extract_first()
        item['zip_code'] = address.xpath('//span[@class="c-address-postal-code"]/text()').extract_first()
        item['country'] = address.xpath('//abbr[@class="c-address-country-name c-address-country-us"]/text()').extract_first()

        item['phone_number'] = left_content.xpath('//div[@class="nap-content-phone"]/div[@class="c-phone-number c-phone-main-number"]/a[@class="c-phone-number-link c-phone-main-number-link"]/text()').extract_first()

        hour_list = []
        hours = response.xpath('//div[@class="nap-content-col-white-right"]/div[@class="nap-content-hours hidden-xs"]/div[@class="c-location-hours"]/div/table/tbody/tr')
        for hour in hours:
            day = hour.xpath('./td[@class="c-location-hours-details-row-day"]/text()').extract_first()
            time = hour.xpath('./td[@class="c-location-hours-details-row-intervals"]/div')
            hour_list.append(day + ' ' + time.xpath('./span[@class="c-location-hours-details-row-intervals-instance-open"]/text()').extract_first() + ' - ' + time.xpath('./span[@class="c-location-hours-details-row-intervals-instance-close"]/text()').extract_first())

        item['store_hours'] = "; ".join(hour_list)
        
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


        

