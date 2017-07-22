from __future__ import unicode_literals
import scrapy
import json
import os
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from chainxy.items import ChainItem
from lxml import etree
from selenium import webdriver
from lxml import html
import usaddress
import pdb
import time

class audiology(scrapy.Spider):
	name = 'audiology'
	domain = 'https://www.audiology.org/'

	def __init__(self):
		self.driver = webdriver.Chrome("./chromedriver")

	def start_requests(self):
		url="http://memberportal.audiology.org/Directories/Find-an-Audiologist?protected=false"
		yield scrapy.Request(url=url, callback=self.body)
	
	def body(self, response):
		self.driver.get("http://memberportal.audiology.org/Directories/Find-an-Audiologist?protected=false")
		self.driver.find_element_by_id('dnn_ctr2708_Find_ctl00_uscSearchForm_pnlFields_i0_i0_rcbLeft_Input').send_keys('U')
	  	self.driver.find_element_by_id('dnn_ctr2708_Find_ctl00_btnSearch').click()
		source = self.driver.page_source.encode("utf8")
		tree = etree.HTML(source)
		number = tree.xpath('.//span[@id="dnn_ctr2708_Find_ctl00_ListPagerControl_lblPageNumber"]/text()')[0]
		if number == '1':
			store_list = tree.xpath('//div[contains(@class, "aaaDirectoryList")]')
			for store in store_list:
				item = ChainItem()
				item['store_name'] = store.xpath('.//span[@class="aaaNameSpan aaaLabelName"]/text()')[0]
				item['store_number'] = ''
				try:
					item['address'] = self.validate(store.xpath('.//div[@class="aaaDirectoryAddress"]/a/p[1]/span/text()'))[0]
				except:
					item['address'] = ''

				try:
					address = self.validate(store.xpath('.//div[@class="aaaDirectoryAddress"]/a/p[2]/span/text()'))[0].replace('&nbsp;', '')
					item['city'] = address.split(',')[0]
					item['state'] = address.split(',')[1].strip().split(' ')[0]
					item['zip_code'] = address.split(',')[1].strip().split(' ')[1]
				except:
					item['city'] = ''
					item['state'] = ''
					item['zip_code'] = ''
				item['phone_number'] = store.xpath('.//div[@class="aaaDirectoryAddress"]/p/span/text()')[0]
				item['country'] = 'United States'
				item['store_hours'] = ''
				yield item	
		
  		self.driver.find_element_by_id('dnn_ctr2708_Find_ctl00_ListPagerControl_lnkNext').click()
  		time.sleep(1)
		store_list = tree.xpath('//div[contains(@class, "aaaDirectoryList")]')
		for store in store_list:
			item = ChainItem()
			item['store_name'] = self.validate(store.xpath('.//span[@class="aaaNameSpan aaaLabelName"]/text()')[0])
			item['store_number'] = ''
			try:
				item['address'] = self.validate(store.xpath('.//div[@class="aaaDirectoryAddress"]/a/p[1]/span/text()'))[0]
			except:
				item['address'] = ''

			try:
				address = self.validate(store.xpath('.//div[@class="aaaDirectoryAddress"]/a/p[2]/span/text()'))[0].replace('&nbsp;', '')
				item['city'] = address.split(',')[0]
				item['state'] = address.split(',')[1].strip().split(' ')[0]
				item['zip_code'] = address.split(',')[1].strip().split(' ')[1]
			except:
				item['city'] = ''
				item['state'] = ''
				item['zip_code'] = ''

			item['phone_number'] = store.xpath('.//div[@class="aaaDirectoryAddress"]/p/span/text()')[0]
			item['country'] = 'United States'
			item['store_hours'] = ''
			yield item	

	def validate(self, item):
		try:
			return item.strip().replace(u'\xa0', ' ')
		except:
			return ''

