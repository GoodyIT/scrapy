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

class Hannaford(scrapy.Spider):
    name = "hannaford"

    domain = "http://www.hannaford.com/custserv/locate_store.cmd/"
    start_urls = ["http://www.hannaford.com/custserv/locate_store.cmd"]
    store_id = []

    # calculate number of pages
    def parse(self, response):
        store_list = response.body.split('map = new google.maps.Map(document.getElementById("map"), myOptions);')[1].strip().split('for (var i = 0;')[0].strip().split("var t = new Object();")
        for store_info in store_list:
            if store_info == '':
                continue

            item = ChainItem()
            store = store_info.strip()
            item['zip_code'] = re.search(r't.zip = "(.*)"', store).group(1)

            item['store_number'] = re.search(r't.number = "(.*)"', store).group(1)
            
            item['store_name'] = re.search(r't.name = "(.*)"', store).group(1)
            item['city'] = re.search(r't.city = "(.*)"', store).group(1)
            item['state'] = re.search(r't.state = "(.*)"', store).group(1)
            item['zip_code']
            item['address'] = re.search(r't.address1 = "(.*)"', store).group(1)
            item['address2'] = re.search(r't.address2 = "(.*)"', store).group(1)
            item['phone_number'] = re.search(r't.phone = "(.*)"', store).group(1)
            item['latitude'] = re.search(r't.lat = (.*)', store).group(1).strip()[:-1]
            item['longitude'] = re.search(r't.lng = (.*)', store).group(1).strip()[:-1]

            response = requests.post(url=self.start_urls[0], data={ "cityStateZip": item['zip_code']})
            try:
                item['store_hours'] = ";".join(response.xpath('//div[@class="storeHours"]')[0].xpath('.//p/text()').extract())
            except:
                item['store_hours'] = ''

            yield item




        

