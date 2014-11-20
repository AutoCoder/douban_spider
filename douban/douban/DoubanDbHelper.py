'''
Begin Modify on 2014.11.19

@author: tj_liyuan

'''
import MySQLdb
from scrapy import log

class DoubanDbHelper(object):
    
    @staticmethod
    def SetupDoubanSchema(conn):
        try:
            if conn is None:
                log.msg("[SetupDoubanSchema()] the conn argument is None!", log.ERROR)
                return
            cur = conn.cursor()
            cur.execute('create database if not exists Douban DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin')
            conn.commit()   
             
            conn.select_db('Douban')
            cur=conn.cursor()
            createtable_sql1 = """CREATE TABLE IF NOT EXISTS bbs_topics (Id INT PRIMARY KEY AUTO_INCREMENT,
                                                     title TEXT NOT NULL, 
                                                     author varchar(30) NOT NULL,
                                                     author_page_link varchar(100) NOT NULL,
                                                     content TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL, 
                                                     comments_count INT, 
                                                     image_count INT, 
                                                     douban_topic_id varchar(10),
                                                     douban_topic_link varchar(100),
                                                     latest_comment_timestamp TIMESTAMP NOT NULL,
                                                     post_timestamp TIMESTAMP NOT NULL) 
                                                     ENGINE = InnoDB 
                                                     DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;"""
            createtable_sql2 = """CREATE TABLE IF NOT EXISTS topic_comments (Id INT PRIMARY KEY AUTO_INCREMENT,
                                                     douban_topic_link varchar(100) NOT NULL, 
                                                     content TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL , 
                                                     author varchar(30) NOT NULL,
                                                     author_page_link varchar(100) NOT NULL,
                                                     quote_author varchar(30), 
                                                     quote_author_link varchar(100), 
                                                     quote_content TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin, 
                                                     post_timestamp TIMESTAMP NOT NULL, 
                                                     up_count INT DEFAULT 0, 
                                                     quote_count INT DEFAULT -1) 
                                                     ENGINE = InnoDB
                                                     DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;"""
            addindex_sql = """ALTER TABLE `bbs_topics` ADD INDEX `idx_douban_topic_link` (`douban_topic_link` ASC);"""
#                                  ALTER TABLE `topic_comments` ADD CONSTRAINT `topic_id`
#                                     FOREIGN KEY (`douban_topic_link`)
#                                     REFERENCES `bbs_topics` (`douban_topic_link`)
#                                     ON DELETE NO ACTION
#                                     ON UPDATE NO ACTION;
#
            #Use utf8mb4-utf8mb4_bin is for support 'emoji' face gif
            cur.execute(createtable_sql1)
            conn.commit()
            cur.execute(createtable_sql2)
            conn.commit()
            cur.execute(addindex_sql)
            conn.commit()
        except MySQLdb.Error,e:
            log.msg("Mysql Error %d: %s" % (e.args[0], e.args[1]), log.ERROR)
    
    @staticmethod
    def InsertHaixiuItem(conn, item):
        try:
            if conn is None:
                log.msg("[InsertHaixiuItem()] the conn argument is None!", log.ERROR)
                return
            
            cur = conn.cursor()
            setcharset_sql = u"""SET NAMES utf8mb4;"""
            cur.execute(setcharset_sql)
            conn.commit()
            insert_sql = u""" INSERT INTO bbs_topics (title,
                                                         author,
                                                         author_page_link, 
                                                         content, 
                                                         comments_count, 
                                                         image_count, 
                                                         douban_topic_id, 
                                                         douban_topic_link, 
                                                         latest_comment_timestamp, 
                                                         post_timestamp) VALUES ("%s", "%s", "%s", "%s", %d, %d, "%s", "%s", "%s", "%s")
            """ % (DoubanDbHelper.__escape(item["title"]), DoubanDbHelper.__escape(item["author"]), item["author_page_link"], DoubanDbHelper.__escape(item["content"]), item["comments_count"], \
                   item["image_count"], item["douban_topic_id"], item["douban_topic_link"], item["latest_comment_timestamp"], (item["post_timestamp"]))
            cur.execute(insert_sql)
            conn.commit()
            
        except MySQLdb.Error,e:
            log.msg("[Content]: %s" % (conn.escape_string(item["content"].encode('utf8')).decode('utf8')), log.ERROR)
            log.msg("Mysql Error %d: %s" % (e.args[0], e.args[1]), log.ERROR)
    
    
    @staticmethod 
    def InsertHaixiuCommentItem(conn, item):
        try:
            if conn is None:
                log.msg("[InsertHaixiuCommentItem()] the conn argument is None!", log.ERROR)
                return
            
            cur = conn.cursor()
            setcharset_sql = u"""SET NAMES utf8mb4;"""
            cur.execute(setcharset_sql)
            conn.commit()
            
            insert_sql = u"""INSERT INTO topic_comments (douban_topic_link,
                                                         content,
                                                         author, 
                                                         author_page_link, 
                                                         quote_author, 
                                                         quote_author_link, 
                                                         quote_content, 
                                                         post_timestamp, 
                                                         up_count) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", %d)
            """ % (item["douban_topic_link"], DoubanDbHelper.__escape(item["content"]), DoubanDbHelper.__escape(item["author"]), item["author_page_link"], DoubanDbHelper.__escape(item["quote_author"]), \
                   item["quote_author_link"], DoubanDbHelper.__escape(item["quote_content"]), item["post_timestamp"], item["up_count"])
                               
            cur.execute(insert_sql)
            conn.commit()
                    
        except MySQLdb.Error,e:
            log.msg("[Content]: %s" % (conn.escape_string(item["content"].encode('utf8')).decode('utf8')), log.ERROR)
            log.msg("Mysql Error %d: %s" % (e.args[0], e.args[1]), log.ERROR)
            
    @staticmethod
    def __escape(itemattr):
        return MySQLdb.escape_string(itemattr.encode('utf8')).decode('utf8')