__author__ = 'brian'

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.loader import ItemLoader
from ..items import PostItem, AuthorItem, TestItem

# scrapy crawl ninfo -o myinfo.csv -t csv

def parse_urls():
        my_url_list = []
        with open('url_list.txt', 'r') as f:
            my_url_list = f.read().strip().split(',')
        return my_url_list

class DepthSpider(CrawlSpider):

    name = "depth"
    download_delay = 2
    allowed_domains = ["footballsfuture.com"]
    start_urls = parse_urls()

    pipelines = ['']

    rules = (
        # restrict_xpaths =('//span/a[@class = "forumlink]'),callback=('parse_items')
        Rule(LinkExtractor(restrict_xpaths=('//span/a[@class = "forumlink"]'),
                           allow=(r'http://www.footballsfuture.com/phpBB2/viewforum\.php\?f='), ), ),
        Rule(LinkExtractor(restrict_xpaths=('//span/a[@class = "topictitle"]'), ),
             callback='parse_item', follow=True, ),
        Rule(LinkExtractor(restrict_xpaths=('//span[@class = "nav"]/a[text()="Next"]'), ),
             callback='parse_item', follow=True, ),

    )


    def parse_item(self, response):
        # select_names = response.selector.xpath('//tr/td/span[@class="name"]/b').extract()


        # create itemloader and send xpaths
        # l1 = ItemLoader(item=PostItem(), response=response)
        # l1.add_xpath('user_name', '//tr/td/span[@class="name"]/b')
        # l1.add_xpath('date', '//tr/td[@width="100%"][1]/span[@class = "postdetails"]/text()')
        # l1.add_xpath('content')
        # l1.add_xpath('team', '//tr/td[2]/span[@class = "nav"]/a[@class = "nav"][2]/text()')

        #post_title = scrapy.Field()
        #page = scrapy.Field()
        #team = scrapy.Field()
        #date = scrapy.Field()
        # abc = datetime.strptime(select_date[0][8:], "%a %b %d, %Y %H:%M %p")
        l1 = ItemLoader(item=TestItem(), response=response)
        l1.add_xpath('post_title', '//tr/td/a[@class = "maintitle"]/text()')
        l1.add_xpath('date', '//tr/td[@width="100%"][1]/span[@class = "postdetails"]/text()')
        l1.add_xpath('team', '//tr/td[2]/span[@class = "nav"]/a[@class = "nav"][2]/text()')
        l1.add_xpath('page', '//tr/td/span[@class = "gensmall"]/b/b/text()')
        return l1.load_item()


        # l2 = ItemLoader(item=AuthorItem(), response=response)
        # l2.add_xpath('user_name', '//tr/td/span[@class="name"]/b')
        # l2.add_xpath('geo_location')
        # l2.add_xpath('num_posts')


        #Page num response.selector.xpath('//tr/td/span[@class = "gensmall"]/b/b/text()').extract()

        # #TODO clean body data
        # select_bodies = response.selector.xpath('//tr/td/span[@class="postbody"]/text()').extract()
        # select_title = response.selector.xpath('//tr/td/a[@class = "maintitle"]/text()').extract()
        # #TODO: select first() for topic
        # select_team = response.selector.xpath('//tr/td[2]/span[@class = "nav"]/a[@class = "nav"][2]/text()').extract()
        # #TODO: format date
        # select_date = response.selector.xpath('//tr/td[@width="100%"][1]/span[@class = "postdetails"]/text()').extract()
        #
        # for idx, name in select_names:
        #     pass



