'''
Created on 2014.11.17

@author: tj_liyuan
'''

from scrapy.spider import Spider
from scrapy import log
from datetime import date
from douban.settings import ProjectDir#, BasicDir
# import json
# import sys

class BaseSpider(Spider):
    def __init__(self):
        log.start('%s/ScrapyHistory/%s/%s.log' % (ProjectDir, self.name, str(date.today())), loglevel=log.INFO, logstdout=False)        
            #configfile = open(BasicDir + "/crawl_conf.json",'r')
            #for line in configfile.readlines():
                #print line
            #self.configdict = json.load(configfile, encoding='utf-8')
            
#             print "init basespider"
#         except Exception, info: #IndexError
#             s=sys.exc_info()                             
#             log.msg("[haixiu] Error '%s' happened on line %d" % (s[1],s[2].tb_lineno), log.ERROR)
#             #log.msg('[jd_milk] prod_link : %s' % prod_link, log.ERROR)
#             print "init basespider12"