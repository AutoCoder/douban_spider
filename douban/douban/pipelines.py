'''
Begin Modify on 2014.11.18

@author: tj_liyuan

'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from douban.items import HaixiuItem, HaixiuCommentItem
from douban.DoubanDbHelper import DoubanDbHelper
import MySQLdb
from scrapy import log

class DoubanPreprocessPipeline(object):
    """
        if there are no database created, this pipeline will create the database
    """
    def process_item(self, item, spider):
        return item
    
    def open_spider(self, spider):
        #read db configuration from settings
        conn = MySQLdb.connect(host="127.0.0.1", user='spider',passwd='wodemima',port=3306, charset='utf8')
        DoubanDbHelper.SetupDoubanSchema(conn)
        conn.close()


class DoubanStore2DbPipeline(object):
    def __init__(self):
        self.conn = None
            
    def open_spider(self, spider):
        try:
            self.conn=MySQLdb.connect(host="127.0.0.1", user='spider',passwd='wodemima',port=3306, charset='utf8')
            self.conn.select_db('Douban')
            self.conn.set_character_set('utf8mb4')

        except MySQLdb.Error,e:
            log.msg("Mysql Error %d: %s" % (e.args[0], e.args[1]), log.ERROR)


    def process_item(self, item, spider):
        
        if (type(item) is HaixiuItem):
            DoubanDbHelper.InsertHaixiuItem(self.conn, item)
        elif (type(item) is HaixiuCommentItem):
            DoubanDbHelper.InsertHaixiuCommentItem(self.conn, item)

        return item


    def close_spider(self, spider):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None