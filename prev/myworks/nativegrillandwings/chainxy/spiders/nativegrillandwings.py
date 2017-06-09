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

class Nativegrillandwings(scrapy.Spider):
    name = "nativegrillandwings"

    domain = "https://nativegrillandwings.com/"
    start_urls = ["https://nativegrillandwings.com/locations/"]
    store_id = []

    def parse(self, response):
        store_link = response.xpath('.//div[contains(@class, "so-panel widget widget_black-studio-tinymce widget_black_studio_tinymce")]//div[@class="textwidget"]/h3/a')
        for url in store_link:
            request = scrapy.Request(url=url.xpath('.//@href').extract_first(), callback=self.parse_store)
            request.meta['store_name'] = url.xpath('.//text()').extract_first()
       
            yield request

    # with open('res.html', 'wb') as f:
    #     f.write(links)
    # return

    def parse_store(self, response):
        item = ChainItem()

        item['store_number'] = ''
        item['store_name'] = response.meta['store_name'].replace(u'\u2013', '-')
        item['city'] = response.xpath('.//div[@class="wpsl-location-address"]/span[2]/text()').extract_first()
        item['state'] = response.xpath('.//div[@class="wpsl-location-address"]/span[3]/text()').extract_first()
        item['zip_code'] = response.xpath('.//div[@class="wpsl-location-address"]/span[4]/text()').extract_first()
        item['address'] = response.xpath('.//div[@class="wpsl-location-address"]/span[1]/text()').extract_first()
        item['address2'] = ''
        item['country'] = 'United States'
        item['phone_number'] = self.validate(response.xpath('.//div[@class="wpsl-contact-details"]/span[1]/text()').extract_first())

        item['latitude'] = ''
        item['longitude'] = ''

        hours = response.xpath('.//table[@class="wpsl-opening-hours"]/tr')
        item['store_hours'] = ''
        for hour in hours:
            item['store_hours'] += hour.xpath('.//td[1]/text()').extract_first() + ' ' +  hour.xpath('.//td[2]/time/text()').extract_first() + "; "
        item['other_fields'] = ""
        item['coming_soon'] = "0"
        if item['store_name'].find('- COMING SOON!') != -1:
            item['coming_soon'] = "1"
            item['store_name'] = item['store_name'].replace('- COMING SOON!', '').strip()
            
        yield item

    def validate(self, value):
        if value == None:
            return ""
        else:
            return value




        

