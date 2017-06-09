import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class JimmychooSpider(scrapy.Spider):
    name = "jimmychoo"

    start_urls = ['https://row.jimmychoo.com/de_DE/store-locator#country=US&address=USA&format=ajax']
    request_url = "$$url$$&dwfrm_storelocator_findbycountry=ok"
    base_url = 'https://row.jimmychoo.com'
    storeNumbers = []

    def hasNumbers(self, inputString):
        return any(char.isdigit() for char in inputString)

    def parse(self, response):
        url = response.xpath('.//form[@id="dwfrm_storelocator"]/@action').extract_first()

        formdata = {
            'country':'US',
            'address':'USA',
            'format':'ajax'
        }

        yield FormRequest(url=self.request_url.replace('$$url$$', url), formdata=formdata, callback=self.parse_store)

    def parse_store(self, response):
        # get total number of stores
        stores = response.xpath('//div[@class="storelocator-result js-store-line baseline-huge clearfix js-store-information"]')
        for store in stores:
            try:
                item = ChainItem()
                item['store_name'] = store.xpath(".//div[@class='store-name']/a/text()").extract_first().strip()
                item['store_number'] = store.xpath(".//div[@class='store-name']/a/@href").extract_first().strip().split('?')[1].replace('StoreID=', '')
                url = store.xpath(".//div[@class='store-name']/a/@href").extract_first().strip()
                item['address'] = ''
                item['address2'] = ""
                try:
                    item['phone_number'] = store.xpath('.//div[@class="store-result-address"]/div[5]/a/text()').extract_first().strip()
                except:
                    item['phone_number'] = store.xpath('.//div[@class="store-result-address"]/div[4]/a/text()').extract_first().strip()

                latlng = json.loads(store.xpath('@data-marker-info').extract_first())
                item['latitude'] = latlng['latitude']
                item['longitude'] = latlng['longitude']
                item['city'] = store.xpath('.//div[@class="store-result-address"]/text()').extract()[1].strip()
                item['state'] =  store.xpath('.//div[@class="store-result-address"]/div[2]/text()').extract_first().strip()
                item['zip_code'] = store.xpath('.//div[@class="store-result-address"]/div[3]/text()').extract_first().strip().replace('HI', '')

                if self.hasNumbers(item['state']):
                    item['zip_code'] = item['state']
                    item['state']= ''

                if 'New York,' in item['city']:
                    item['state']= 'NY'

                if 'COSTA MESA' in item['city']:
                    item['state']= 'CA'

                if item['city'].strip() == '':
                    item['city'] = item['store_name']

                item['country'] = 'United States'    
                if 'San Juan' in item['city']:
                    item['state'] = ''
                    item['city'] = 'San Juan'
                    item['country'] = 'Puerto Rico'


                hourStr = ''
                item['store_hours'] = hourStr
                item['city'] = item['city'].replace(',', '')
                # item['store_type'] = store.xpath('.//div[@class="store-type"]/text()').extract_first()
                item['other_fields'] = ""
                item['coming_soon'] = "0"

                request = scrapy.Request(url=self.base_url+url, callback=self.parse_hour)
                request.meta['item'] = item
                yield request
            except:
                # pdb.set_trace()
                continue

    def parse_hour(self,response):
        try:
            item = response.meta['item']
            item['address'] = response.xpath("//p[contains(@class, 'baseline-none')][2]/text()").extract_first()
            if self.hasNumbers(item['address']) == False:
                item['address'] = response.xpath("//div[contains(@class, 'baseline-medium')]/p[contains(@class, 'baseline-none')][1]/text()").extract_first().replace('\r', '').replace('\n', '')#.split(',')[1]

            item['store_hours'] = '; '.join(response.xpath("//div[contains(@class, 'column column-50 last store-hours')]/p/text()").extract()).replace('\r', '').replace('\n', '').replace('br/>', '')
            yield item
        except:
            # pdb.set_trace()
            pass



