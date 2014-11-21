'''
Created on 2014.11.17

@author: tj_liyuan
'''

from scrapy.spider import Spider
from scrapy import log
from datetime import date
import json
import os

BasicDir = os.path.dirname(os.path.dirname(__file__))
ProjectDir = os.path.dirname(BasicDir)
configdir = BasicDir + "/conf"

class BaseSpider(Spider):
    def __init__(self):
        log.start('%s/ScrapyHistory/%s/%s.log' % (ProjectDir, self.name, str(date.today())), loglevel=log.INFO, logstdout=False)        
        configfile = open(configdir + "/dataconfig",'r')
        configdict = json.load(configfile, encoding='utf-8')
        
