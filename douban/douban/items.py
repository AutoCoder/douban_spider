# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class DoubanItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class HaixiuItem(Item):
    uuid = Field()
    title = Field()
    author = Field()
    author_page_link = Field()
    content = Field()
    comments_count = Field()
    post_timestamp = Field()
    douban_topic_id = Field()
    douban_topic_link = Field()
    latest_comment_timestamp = Field()
    image_count = Field()
    
class HaixiuCommentItem(Item):
    uuid = Field()
    content = Field()
    author = Field()
    author_page_link = Field()
    quote_author = Field()
    quote_content = Field()
    post_timestamp = Field()
    up_count = Field()
    quote_count = Field()
    