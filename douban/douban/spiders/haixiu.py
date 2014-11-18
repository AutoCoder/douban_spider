'''
Created on 2014.11.17

@author: tj_liyuan
'''

from scrapy.spider import Spider
from scrapy import log
from datetime import datetime

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.exceptions import DropItem
#from spiderutility import SpiderUtility
from douban.items import HaixiuItem, HaixiuCommentItem
from douban.spiders.basespider import BaseSpider
from douban.utility import Utility

import sys
import uuid
import re

class Haixiu_Spider(BaseSpider):
    name = "haixiu"
    allowed_domains = ["www.douban.com"]
    start_urls = []
    for page_idx in xrange(10):
        start_urls.append("http://www.douban.com/group/haixiuzu/discussion?start=%d" % page_idx)
    
    def __init__(self):
        super(Spider, self).__init__()
    
    def parse(self, response):
        """
        This function will parse the catalogue of haixiu zu and extract the topic link to parse deeply
        @url http://www.douban.com/group/haixiuzu/discussion?start={page_idx}
        @scrapes haixiu
        """
        #sel = Selector(response)
        sel = Selector(None, response.body_as_unicode().replace('\t','').replace('\r','').replace('\n',''), 'html') #avoid the html contain "\n", "\r" , which will caused the xpath doesn't work well
        listdata = sel.xpath('//tr[@class!="th" and not(@id)]')
        
        try:
            for topic in listdata:
                item = HaixiuItem()
                item["title"] = topic.xpath('td[@class="title"]/a/@title').extract()[0]
                item["douban_topic_link"] = topic.xpath('td[@class="title"]/a/@href').extract()[0]
                item["douban_topic_id"] = item["douban_topic_link"].split(u'/')[-2]
                item["author_page_link"] = topic.xpath('td[2]/a/@href').extract()[0]
                item["author"] = topic.xpath('td[2]/a/text()').extract()[0]
                comment_count_node = topic.xpath('td[3]/text()').extract()
                if comment_count_node:
                    item["comments_count"] = int(comment_count_node[0])
                else:
                    item["comments_count"] = 0
                post_datetime_str = "%d-%s" % (datetime.today().year, topic.xpath('td[last()]/text()').extract()[0])
                item["latest_comment_timestamp"] = Utility.Timestr2Timestamp(post_datetime_str, "%Y-%m-%d %H:%M")
    
                yield Request(url=item["douban_topic_link"], meta={'item':item}, callback=self.parse_topic)
        except Exception, info: #IndexError
                s=sys.exc_info()                             
                log.msg("[haixiu] Error '%s' happened on line %d" % (s[1],s[2].tb_lineno), log.ERROR)
                #log.msg('[jd_milk] prod_link : %s' % prod_link, log.ERROR)
                log.msg('[haixiu] item : %s' % item, log.ERROR)


    def parse_topic(self, response):
        try:
            item = response.meta['item']
            sel = Selector(None, response.body_as_unicode().replace('\t','').replace('\r','').replace('\n',''), 'html')

            #parse topic related info
            post_time_str = sel.xpath('//div[@class="topic-doc"]/h3/span[@class="color-green"]/text()').extract()[0]
            item["post_timestamp"] = Utility.Timestr2Timestamp(post_time_str)
            
            item["content"] = sel.xpath('//div[@class="topic-content"]').extract()[0]

            yield item
            yield Request(url=item["douban_topic_link"] + "?start=0", meta={'topic':item["douban_topic_link"]}, callback=self.parse_comment)

        except Exception, info: #IndexError
            s=sys.exc_info()
            log.msg("[haixiu] Error '%s' happened on line %d" % (s[1],s[2].tb_lineno), log.ERROR)
            #log.msg('[jd_milk] prod_link : %s' % prod_link, log.ERROR)
            log.msg('[haixiu] item : %s' % item, log.ERROR)
    
    
    def parse_comment(self, response):
        sel = Selector(None, response.body_as_unicode().replace('\t','').replace('\r','').replace('\n',''), 'html')
        topic_link = response.meta['topic']

        comments_nodes = sel.xpath('//ul[@id="comments" and @class="topic-reply"]/li')
        for comment_node in comments_nodes:
            try:
                cm_item = HaixiuCommentItem()
                cm_item["douban_topic_link"] = topic_link
                inner_comment_node = comment_node.xpath('div[@class="reply-doc content"]')
                cm_item["content"] = inner_comment_node.xpath('p/text()').extract()[0]
                cm_item["author"] = inner_comment_node.xpath('div[@class="bg-img-green"]/h4/a/text()').extract()[0]
                cm_item["author_page_link"]= inner_comment_node.xpath('div[@class="bg-img-green"]/h4/a/@href').extract()[0]
                
                quote_node = comment_node.xpath('div[@class="reply-quote"]')
                if quote_node:
                    cm_item["quote_content"] = quote_node.xpath('span[@class="all"]').extract()[0]
                    cm_item["quote_author"] = quote_node.xpath('span[@class="pubdate"]/a/text()').extract()[0]
                    cm_item["quote_author_link"] = quote_node.xpath('span[@class="pubdate"]/a/@href').extract()[0]
                    pass
                else:
                    cm_item["quote_author"] = ""
                    cm_item["quote_content"] = ""
                    cm_item["quote_author_link"] = ""
                    
                reply_time_str = inner_comment_node.xpath('div[@class="bg-img-green"]/h4/span[@class="pubtime"]/text()').extract()[0]
                cm_item["post_timestamp"] = Utility.Timestr2Timestamp(reply_time_str)
                up_count_str = inner_comment_node.xpath('div[@class="operation_div"]/a[@class="comment-vote lnk-fav"]/text()').extract()[0]
                cm_item["up_count"] = self.__extractUpCount(up_count_str)
                cm_item["quote_count"] = -1
                yield cm_item;
                
            except Exception, info: #IndexError
                s=sys.exc_info()
                log.msg("[haixiu] Error '%s' happened on line %d" % (s[1],s[2].tb_lineno), log.ERROR)
                #log.msg('[jd_milk] prod_link : %s' % prod_link, log.ERROR)
                log.msg('[haixiu] item : %s' % cm_item, log.ERROR) 
        
        next_url_node = sel.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href')#
        next_url = next_url_node.extract()[0] if next_url_node else None
        if next_url:        
            yield Request(url=next_url, meta={'uuid': uuid}, callback=self.parse_comment)
                
    def parse_comment_conent(self, html):
        item = HaixiuCommentItem()
        yield item
    
    
    def __unicode__(self):
        return unicode(self.name)
    
    def __extractUpCount(self, up_str):
        m = re.match(ur"\((\d+)\)", up_str)
        if m:
            return m.group(1)
        else: 
            return 0