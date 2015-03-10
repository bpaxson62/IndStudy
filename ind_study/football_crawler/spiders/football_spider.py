
__author__ = 'brian'

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.loader import ItemLoader
from ..items import PostItem, AuthorItem



class FootballSpider(CrawlSpider):
    name = "football"
    allowed_domains = ["footballsfuture.com"]
    start_urls = [
        "http://www.footballsfuture.com/phpBB2/"
    ]

    pipelines = ['SQLPipeline']
    
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

        #abc = datetime.strptime(select_date[0][8:], "%a %b %d, %Y %H:%M %p")
        # abc
        # datetime.datetime(2014, 10, 24, 1, 20)

    def parse_item(self, response):


        select_names = response.selector.xpath('//tr/td/span[@class="name"]/b').extract()

       # a = response.selector.xpath('//tr/td[@width="100%"][1]/span[@class = "postdetails"]/text()').extract();

        # if(len(a)!=15 and len(a)!=0 and select_names == 15):
        #     print('fail!')


        #create itemloader and send xpaths
        l1 = ItemLoader(item=PostItem(), response=response)
        l1.add_xpath('user_name','//tr/td/span[@class="name"]/b')
        l1.add_xpath('date', '//tr/td[@width="100%"][1]/span[@class = "postdetails"]/text()')
        l1.add_xpath('content')
        l1.add_xpath('team', '//tr/td[2]/span[@class = "nav"]/a[@class = "nav"][2]/text()')

        l1.add_xpath('post_title', '//tr/td/a[@class = "maintitle"]/text()')

        l2 = ItemLoader(item=AuthorItem(), response=response)
        l2.add_xpath('user_name', '//tr/td/span[@class="name"]/b')
        l2.add_xpath('geo_location')
        l2.add_xpath('num_posts')


        #TODO clean body data
        select_bodies = response.selector.xpath('//tr/td/span[@class="postbody"]/text()').extract()
        select_title = response.selector.xpath('//tr/td/a[@class = "maintitle"]/text()').extract()
        #TODO: select first() for topic
        select_team = response.selector.xpath('//tr/td[2]/span[@class = "nav"]/a[@class = "nav"][2]/text()').extract()
        #TODO: format date
        select_date = response.selector.xpath('//tr/td[@width="100%"][1]/span[@class = "postdetails"]/text()').extract()

        for idx, name in select_names:
            pass

        #forum page num [0]=current [1] = max response.selector.xpath('//tr/td[@align="left" and @colspan="3"]/span[@class = "nav"]/b/text()').extract()
        #forum title response.selector.xpath('//tr/td/a[@class = "maintitle"]/text()').extract()
        #forum topic response.selector.xpath('//tr/td[2]/span[@class = "nav"]/a[@class = "nav"][2]/text()').extract()
        #forum date response.selector.xpath('//tr/td[@width="100%"][1]/span[@class = "postdetails"]/text()').extract()
        #forum body response.selector.xpath('//tr/td[not(@class="quote")]/span[@class="postbody" and text()]')

        # r = re.compile(r'(\d)')
        # a = Selector(text=body).xpath('//span/a[@class = 'forumlink']/@href').re.search(r, ' ')

        # a.extract()
        # for iter in a:
        #     print(iter.re(r))
        # filename = response.url.split("/")[-2]
        # with open(filename, 'wb') as f:
        #     f.write(response.body)