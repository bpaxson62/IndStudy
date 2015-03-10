# -*- coding: utf-8 -*-

# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'football_crawler'

SPIDER_MODULES = ['football_crawler.spiders']
NEWSPIDER_MODULE = 'football_crawler.spiders'
# ITEM_PIPELINES = {'football_crawler.pipelines.SQLPipeline': 1,
# }

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tutorial (+http://www.yourdomain.com)'
