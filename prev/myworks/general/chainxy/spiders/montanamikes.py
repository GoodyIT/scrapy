import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class MontanamikesSpider(scrapy.Spider):
    name = "montanamikes"
    uid_list = []
    
    headers = {
        "Origin":"https://mrsub.ca",
        "Referer":"https://mrsub.ca/locations/",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest",
        "Accept":"*/*",
        "Content-Type":"application/x-www-form-urlencoded"
    }


    def __init__(self):
        states   = open('states.json', 'rb')
        self.states = json.loads(states.read())
    def start_requests(self):
        request_url = "https://montanamikes.com/store-locator/"
        for state in self.states:
            form_data = {
                'wpseo-sl-search':'Illinois',
                'wpseo-sl-radius':'10000',
                '42fbc0a17b19bd1691d13121505ec2fd':'e5a02a4239170a1b0faea454d2d3f265',
                'WP55T3S7XJS2':'7H5W8K53HX'
            }
            request = FormRequest(url=request_url, formdata=form_data, headers=self.headers, callback=self.parse_store)

            yield request

    def parse_store(self, response):
        for store in response.xpath('//div[contains(@class, "wpseo-result")]'):
            # pdb.set_trace()
            
            item = ChainItem()
            item['store_name'] =  store.xpath('.//span[@itemprop="name"]/text()').extract_first().strip()
            pos = store.xpath('.//div[@class="wpseo-sl-route"]/a/@onclick').extract_first()

            item['store_number'] = ''
            item['address'] = self.validate(store.xpath('.//span[@itemprop="streetAddress"]/text()'))
            item['address2'] = ''
            item['city'] = self.validate(store.xpath('.//span[@itemprop="addressLocality"]/text()'))

            item['state'] = self.validate(store.xpath('.//span[@itemprop="addressRegion"]/text()'))

            item['zip_code'] = self.validate(store.xpath('.//span[@itemprop="postalCode"]/text()'))

            item['country'] = 'Canada'
            item['phone_number'] = self.validate(store.xpath('.//span[@itemprop="telephone"]/text()'))
            
            item['latitude'] = pos.split(', \'')[1].split('\'')[0]
            item['longitude'] = pos.split(', \'')[2].split('\'')[0]

            item['store_hours'] = ''
            for hour in store.xpath('.//span[@itemprop="openingHours"]/@content').extract():
                item['store_hours'] += hour.replace(u'\xa0', '') + ' ; '

            item['store_type'] = ''
            item['other_fields'] = ''
            item['coming_soon'] = '0'
            if item['phone_number'] not in self.uid_list:
                self.uid_list.append(item['phone_number'])
                yield item

    def validate(self, xpath_obj):
        try:
            return xpath_obj.extract_first().strip()
        except:
            return ""

