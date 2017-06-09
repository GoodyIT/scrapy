# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ChainItem(Item):
    store_name = Field()
    store_number = Field()
    address = Field()
    address2 = Field()
    city = Field()
    state = Field()
    zip_code = Field()
    country = Field()
    phone_number = Field()
    latitude = Field()
    longitude = Field()
    store_hours = Field()
    other_fields = Field()
    store_type = Field()
    coming_soon = Field()
    
    