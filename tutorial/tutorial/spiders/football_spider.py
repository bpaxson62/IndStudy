__author__ = 'brian'

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors import LinkExtractor
import re


class footballSpider(CrawlSpider):
    name = "football"
    allowed_domains = ["footballsfuture.com"]
    start_urls = [
        "http://www.footballsfuture.com/phpBB2/"
    ]
    partial_url1 = "http://www.footballsfuture.com/phpBB2/"
    rules = (
        # restrict_xpaths =('//span/a[@class = "forumlink]'),callback=('parse_items')
        Rule(LinkExtractor(restrict_xpaths=('//span/a[@class = "forumlink"]'),
                           allow=(r'http://www.footballsfuture.com/phpBB2/viewforum\.php\?f='), ), ),
        Rule(LinkExtractor(restrict_xpaths=('//span/a[@class = "topictitle"]'), ),
             callback='parse_item', follow=True,),
        Rule(LinkExtractor(restrict_xpaths=('//span[@class = "nav"]/a[text()="Next"]'), ),
             callback='parse_item', follow=True,),

        # Rule(LinkExtractor(restrict_xpaths = ('//span[@class = "nav"]/a[@class = "topictitle"]'),),
        # callback = 'parse_item'),


        # navbar xpath :::: response.selector.xpath('//span[@class = "nav"]/a[text()="Next"]').extract()

        #some examples rules
        # Rule(LinkExtractor(allow=('seasoncode\=E\d+\&gamenumber\=\d+\&phasetypecode\=\w+',)),follow=True),
        # Rule(LinkExtractor(allow=('gamenumber\=\d+\&phasetypecode\=\w+\&gamecode\=\d+\&seasoncode\=E\d+',)),callback='parse_item')
    )

    def parse_item(self, response):


        select_names = response.selector.xpath('//tr/td/span[@class="name"]/b').extract()
        #TODO clean body data
        select_bodies = response.selector.xpath('//tr/td/span[@class="postbody"]/text()').extract()
        select_title = response.selector.xpath('//tr/td/a[@class = "maintitle"]/text()').extract()
        #TODO: select first() for topic
        select_team = response.selector.xpath('//tr/td[2]/span[@class = "nav"]/a[@class = "nav"][2]/text()').extract()
        #TODO: format date
        select_date = response.selector.xpath('//tr/td[@width="100%"][1]/span[@class = "postdetails"]/text()').extract()

        for idx, name in select_names:
            pass


        #forum title response.selector.xpath('//tr/td/a[@class = "maintitle"]/text()').extract()
        #forum topic response.selector.xpath('//tr/td[2]/span[@class = "nav"]/a[@class = "nav"][2]/text()').extract()
        #forum date response.selector.xpath('//tr/td[@width="100%"][1]/span[@class = "postdetails"]/text()').extract()
        #forum body response.selector.xpath('//tr/td/span[@class="postbody"]/text()').extract()


        # r = re.compile(r'(\d)')
        # a = Selector(text=body).xpath('//span/a[@class = 'forumlink']/@href').re.search(r, ' ')

        # a.extract()
        # for iter in a:
        #     print(iter.re(r))
        # filename = response.url.split("/")[-2]
        # with open(filename, 'wb') as f:
        #     f.write(response.body)