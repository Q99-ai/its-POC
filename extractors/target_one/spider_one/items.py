# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    text = scrapy.Field()