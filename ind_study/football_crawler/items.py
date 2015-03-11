# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from datetime import datetime

import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst

def parse_date(self, date):
    return datetime.strptime(date[0][8:], "%a %b %d, %Y %H:%M %p").ctime()

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

class DepthItem(scrapy.Item):
    post_title = scrapy.Field()
    page = scrapy.Field(default=1)
    team = scrapy.Field()
    date = scrapy.Field()

class DepthItemLoader(ItemLoader):
    default_input_processor = MapCompose(unicode.strip)
    default_output_processor = TakeFirst()

    team_in = TakeFirst()
    team_out = MapCompose(unicode.strip)

    # date_in = TakeFirst()
    date_out = parse_date

