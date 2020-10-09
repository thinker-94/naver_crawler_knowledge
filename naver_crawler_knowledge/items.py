# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SearchWordItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    duplicateFilterPass = scrapy.Field()
    title = scrapy.Field()
    questionContent = scrapy.Field()
    java = scrapy.Field()
    army = scrapy.Field()
    health = scrapy.Field()
    linux = scrapy.Field()
    samsung = scrapy.Field()


