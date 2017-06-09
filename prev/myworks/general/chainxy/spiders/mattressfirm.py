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
import usaddress

class Mattressfirm(scrapy.Spider):
    name = "mattressfirm"

    domain = "http://www.mattressfirm.com/"
    start_urls = ["https://maps.mattressfirm.com/api/getAutocompleteData"]
    store_link = "https://maps.mattressfirm.com/api/getAsyncLocations?template=searchmap&level=search&radius=100&search=%s"

    store_numbers = []

    # calculate number of pages
    def parse(self, response):
        data=json.loads(response.body)
        zipcode_list = data['data'][1829:]

        for zipCode in zipcode_list:
            url = self.store_link % zipCode
            request = scrapy.Request(url=url, callback=self.parse_store_contents)

            yield request

    # pare store detail page
    def parse_store_contents(self, response):   
        store_lists =json.loads(response.body)['markers']
        store_id_list = html.fromstring(json.loads(response.body)['maplist']).xpath('//script[contains(., "store-id")]/text()')
        
        for index in range(0, len(store_id_list)):       
            item = ChainItem()
            item['store_number'] = store_id_list[index].split("store-id")[1].split("};")[0][5:-5].replace('"', '').strip()
            if item["store_number"] in self.store_numbers:
                continue

            self.store_numbers.append(item["store_number"])

            store = store_lists[index]    
            info =  html.fromstring(store['info']);
            
            item['store_name'] = info.xpath('//div[@class="store-name fc-black ff-sans uppercase"]/a/text()')[0]
            address = info.xpath('//span[@class="block address-1 bold fc-gray"]/text()')[0] + info.xpath('//span[@class="block address-zip bold fc-gray"]/text()')[0]
            addr = usaddress.parse(address)
            city = state = zip_code = address = ''
            for temp in addr:
                if temp[1] == 'PlaceName':
                    city += temp[0].replace(',','') + ' '
                elif temp[1] == 'StateName':
                    state = temp[0].replace(',','')
                elif temp[1] == 'ZipCode':
                    zip_code = temp[0].replace(',','')
                else:
                    address += temp[0].replace(',','') + ' '
            item['address'] = address
            item['country'] = 'United States'
            item['city'] = city
            item['state'] =  state
            item['zip_code'] =  zip_code
            item['phone_number'] = info.xpath('//a[@class="phone"]/span/text()')[0]
            item['latitude'] = self.validate(store, "lat")
            item['longitude'] = self.validate(store, "lng")

            info_hours = info.xpath('//div[@class="hours"]/div[@class="day-hour-row"]/meta/@content')
            item['store_hours'] = "; ".join(info_hours)
            
            yield item

    def validate(self, store, property):
        if property in store:
            return store[property]
        return ""


        

