import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
from lxml import etree
import pdb
import datetime
from time import gmtime, strftime

from lxml import etree
class CowboychickenSpider(scrapy.Spider):
    name = "cowboychicken"
    history = []
        

    def start_requests(self):
        yield  scrapy.Request(url="http://www.cowboychicken.com/locations/", callback=self.parse_state)

    def parse_state(self, response):
        idx = 1
        for store in response.xpath('//div[contains(@class,"locations_content")]'):
            
            item = ChainItem()
            item['store_name'] = store.xpath('.//div[@class="locations_cont_lft_head"]/a/text()').extract_first()
            addr = store.xpath('.//div[@class="locations_cont_lft_head"]/p/text()').extract()
            addr = [tp.strip() for tp in addr if tp.strip() != ""]

            item['store_number'] = ''
            try:
                item['address'] = self.escape(addr[0])
            except:
                item['store_name'] = "Atlanta"
                item['coming_soon'] = 1
                yield item
            item['address2'] = ''
            try:
                item['city'] = self.escape(addr[1].split(',')[0].strip())
                item['state'] = self.escape(addr[1].split(',')[1].strip())
                item['zip_code'] = self.escape(addr[1].split(',')[2].strip())
            except:
                return
            item['country'] = "United States"

            item['phone_number'] = self.escape(addr[2].split(':')[1].strip())
            item['latitude'] = response.xpath('//div[@class="locations_main"]/input[@id="lat'+str(idx)+'"]/@value').extract_first()
            item['longitude'] = response.xpath('//div[@class="locations_main"]/input[@id="lon'+str(idx)+'"]/@value').extract_first()
            item['store_hours'] = store.xpath('.//div[@class="locations_cont_rgt"]/p/text()').extract_first()
            idx += 1
            item['store_type'] = ''
            item['other_fields'] = ''
            item['coming_soon'] = '0'
            if item['address'] not in self.history:
                self.history.append(item['address'])

                yield item

    def escape(self, xpath_obj):
        try:
            return xpath_obj.strip().replace(u'\u2014', '-').replace(u'\xa0', ' ').replace(u'\u2013', '-').replace(u'\u202d', '').replace(u'\u202d', '').replace(u'\u202c', '')
        except:
            return ""


