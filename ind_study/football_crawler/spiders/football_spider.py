__author__ = 'brian'

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from ..items import PostItem, AuthorItem, DepthItemLoader


def parse_urls():
    # my_url_list = []
    with open('url_list.txt', 'r') as f:
        my_url_list = f.read().strip().split(',')
    return my_url_list


class FootballSpider(CrawlSpider):
    name = "football"
    allowed_domains = ["footballsfuture.com"]
    start_urls = parse_urls()
    # start_urls = ['http://www.footballsfuture.com/phpBB2/viewforum.php?f=9']

    pipelines = ['SQLPipeline']

    rules = (
        # allow=(r'http://www.footballsfuture.com/phpBB2/viewforum\.php\?f=')
        # restrict_xpaths =('//span/a[@class = "forumlink]'),callback=('parse_items')
        # Rule(LinkExtractor(restrict_xpaths=('//span/a[@class = "forumlink"]'), ), ),
        Rule(LinkExtractor(restrict_xpaths=('//span/a[@class = "topictitle"]'), ), callback='parse_item',
             follow=True, ),
        Rule(LinkExtractor(restrict_xpaths=('//span[@class = "nav"]/a[text()="Next"]'),
                           allow=(r'http://www.footballsfuture.com/phpBB2/viewforum\.php\?f=')), follow=True, ),
        Rule(LinkExtractor(restrict_xpaths=('//span[@class = "gensmall"]/b/a[text()="Next"]'), ),
             callback='parse_item', follow=True, ),

    )


    def parse_item(self, response):
        select_names = response.selector.xpath('//tr/td/span[@class="name"]/b').extract()
        select_bodies = response.selector.xpath(
            '//td[@class="row2" or @class ="row1" and @width="100%" and @valign="top" and @height="28"]'
            '/table[not(@height="18") and not(@align="center")]')
        select_date = response.selector.xpath('//tr/td[@width="100%"][1]/span[@class = "postdetails"]/text()')
        select_name_date = response.selector.xpath(
            '//tr/td/span[@class="postdetails" and text()[contains(.,"Posts:")]]')

        # check to see if we are getting extra content that we should not be
        if len(select_names) > 15 or len(select_bodies) > 15:
            raise ValueError('names or bodies is greater than 15!!!')


        # divide body data further
        body_list = []
        for idx1, value in enumerate(select_bodies):
            my_text = select_bodies[idx1].extract()
            sel = Selector(text=my_text).xpath(
                '//tr/td[@colspan = "2" and not(@class = "quote")]/span[@class = "postbody"]')
            body_list.extend(sel.extract())


        page_number = response.selector.xpath('//tr/td/span[@class = "gensmall"]/b/b/text()')
        my_page = u'1'
        if page_number:
            my_page = response.selector.xpath('//tr/td/span[@class = "gensmall"]/b/b/text()').extract()

        date_index = 0;
        team = response.selector.xpath('//tr/td[2]/span[@class = "nav"]/a[@class = "nav"][2]/text()').extract()
        post_title = response.selector.xpath('//tr/td/a[@class = "maintitle"]/text()')

        for idx, val in enumerate(select_names):
            # create itemloader and send xpaths
            l1 = DepthItemLoader(item=PostItem(), response=response)
            my_username = select_names[idx]
            l1.add_value('user_name', my_username)
            my_date = select_date[date_index].extract()
            date_index += 2
            l1.add_value('date', my_date)
            l1.add_value('content', body_list[idx])
            l1.add_value('team', team)
            l1.add_value('post_title', post_title)
            l1.add_value('page', my_page)
            l1.add_value('position', idx)

            # author data
            l1.add_value('author_name', my_username)
            l1.add_value('geo_location', 'TODO')
            l1.add_value('num_posts', 0)

            yield l1.load_item()



