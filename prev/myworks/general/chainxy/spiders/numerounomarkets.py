import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class NumerounomarketsSpider(scrapy.Spider):
    name = "numerounomarkets"
    uid_list = []

    def start_requests(self):
        url = 'http://numerounomarkets.com/' 

        yield  scrapy.Request(url=url,  callback=self.parse_store)

    def __init__(self):
        states   = open('states.json', 'rb')
        self.states = json.loads(states.read())

    def parse_store(self, response):
        
        stores = response.xpath('//body/div[1]//table//td/ul/li/text()')
        for idx in xrange(0,len(response.xpath('//body/div[1]//table//td/ul/li/text()'))/2-1):
            pdb.set_trace()
            item = ChainItem()
            store = stores[idx]
            item['store_name'] = store.split(':')[0]
            item['store_number'] = store.split(':')[0].split(' ')[-1]
            item['address'] = stores[idx+1].split(',')[0]
            item['address2'] = ''
            addr = stores[idx+1].split(',')[1:]

            item['phone_number'] = store.split(':')[1]

            item['city'] = addr.replace(u'\xa0', '').strip().split(',')[0].strip()
            item['state'] = addr.replace(u'\xa0', '').strip().split(',')[1].strip().split(' ')[0].strip()
            item['zip_code'] = addr.replace(u'\xa0', '').strip().split(',')[1].strip().split(' ')[-1].strip().replace('TX', '')
            
            item['country'] = "United States"
            item['latitude'] = ''
            item['longitude'] = ''
            item['store_hours'] = ""

            item['other_fields'] = ""
            item['coming_soon'] = "0"
            self.uid_list.append(item["store_number"])
            yield item
