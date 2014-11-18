'''
Begin Modify on 2014.11.18

@author: tj_liyuan

'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from scrapy import log

class DoubanPipeline(object):
    def process_item(self, item, spider):
        return item


class DoubanPreprocessPipeline(object):
    """
        if there are no database created, this pipeline will create the database
    """
    def process_item(self, item, spider):
        return item
    
    def open_spider(self, spider):
        try:
            self.conn=MySQLdb.connect(host="127.0.0.1", user='spider',passwd='wodemima',port=3306, charset='utf8')
            cur=self.conn.cursor()
            cur.execute('create database if not exists Douban') 
            self.conn.commit()   
             

            self.conn.select_db('Douban')
            cur=self.conn.cursor()
            createtable_sql = """CREATE TABLE IF NOT EXISTS bbs_topics (Id INT PRIMARY KEY AUTO_INCREMENT,
                                                     uuid varchar(30) NOT NULL,
                                                     title TEXT NOT NULL, 
                                                     author varchar(30) NOT NULL,
                                                     author_page_link varchar(100) NOT NULL,
                                                     content TEXT NOT NULL, 
                                                     comments_count INT, 
                                                     image_count INT, 
                                                     douban_topic_id varchar(10),
                                                     douban_topic_link varchar(100),
                                                     latest_comment_timestamp TIMESTAMP NOT NULL,
                                                     post_timestamp TIMESTAMP NOT NULL) ENGINE = InnoDB;
                                 ALTER TABLE `bbs_topics` ADD INDEX `idx_douban_topic_link` (`douban_topic_link` ASC);
                                 CREATE TABLE IF NOT EXISTS topic_comments (Id INT PRIMARY KEY AUTO_INCREMENT,
                                                     douban_topic_link varchar(100) NOT NULL, 
                                                     content TEXT NOT NULL, 
                                                     author varchar(30) NOT NULL,
                                                     author_page_link varchar(100) NOT NULL,
                                                     quote_author varchar(30), 
                                                     quote_author_link varchar(100), 
                                                     quote_content TEXT, 
                                                     post_timestamp TIMESTAMP NOT NULL, 
                                                     up_count INT DEFAULT 0, 
                                                     quote_count INT DEFAULT -1) ENGINE = InnoDB;"""
            cur.execute(createtable_sql) 
        except MySQLdb.Error,e:
            log.msg("Mysql Error %d: %s" % (e.args[0], e.args[1]), log.ERROR)