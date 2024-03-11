# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class News163Item(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    pass


class News163Article(scrapy.Item):
    title = scrapy.Field()
    docurl = scrapy.Field()
    tlastid = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    pass