import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem

class Sonnysbbq(scrapy.Spider):
    name = "sonnysbbq"

    domain = "https://www.sonnysbbq.com/"
    start_urls = ["https://www.sonnysbbq.com/locations"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_list = response.xpath('//div[@class="accordion-menu"]/ul/li/a/@href').extract()
        for store in store_list:
            url = "https://sonnysbbq.com" + store
            yield scrapy.Request(url=url, callback=self.parse_store_contents)

    # pare store detail page
    def parse_store_contents(self, response): 
        item = ChainItem()
        item['store_name'] = response.xpath('//div[@class="grid-parent grid-70"]/h1/text()').extract_first()
        item['store_number'] = ''
        address = response.xpath('//div[@id="location-store-info"]/div[1]/div[2]/p/a/text()').extract()
        item['address'] = address[0]
        item['address2'] = ''
        if len(address[1].split(' ')) == 4:
            item['city'] = address[1].split(' ')[0].replace('\n', '') + " " + address[1].split(' ')[1]
            item['zip_code'] = address[1].split(' ')[3]
            item['state'] = address[1].split(' ')[2]
        else:
            item['city'] = address[1].split(' ')[0].replace('\n', '')
            item['zip_code'] = address[1].split(' ')[2]
            item['state'] = address[1].split(' ')[1]
        item['country'] = 'United States'
        item['phone_number'] = response.xpath('//span[@class="hide-on-mobile location-phone"]/text()').extract_first()

        item['latitude'] = ''
        item['longitude'] = ''

        hours = response.xpath('//div[@id="location-store-info"]/div[2]/div[2]/p/text()').extract()
        item['store_hours'] = ""
        for hour in hours:
            item['store_hours'] += hour.replace('\n', '')

        #item['store_type'] = info_json["@type"]
        item['other_fields'] = ""
        item['coming_soon'] = "0"
        

        yield item
            

    def validate(self, xpath_obj):
        
        try:
            return xpath_obj.extract_first().strip()
        except:
            return ""

        

