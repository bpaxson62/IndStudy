# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PostItem(scrapy.Item):
    # define the fields for your item here like:
    user_name = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
    team = scrapy.Field()
    post_title = scrapy.Field()
    position = scrapy.Field()
    page = scrapy.Field()

class AuthorItem(scrapy.Item):
    user_name = scrapy.Field()
    geo_location = scrapy.Field()
    num_posts = scrapy.Field()

class TestItem(scrapy.Item):
    post_title = scrapy.Field()
    page = scrapy.Field()
    team = scrapy.Field()
    date = scrapy.Field()