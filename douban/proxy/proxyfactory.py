#!/usr/bin/env python
#coding=utf-8
import urllib2
import socket 
import requests 
from scrapy.selector import Selector
from js.jshelper import HttpGetwithJsExecuted


class proxyfactory:  

    @staticmethod
    def __testproxy(proxy_dict, url='http://www.douban.com', verifytext=u"2005－2014 douban.com, all rights reserved"):
        """
            The example 3rd arguments:
            proxies = {
              "http": "http://10.10.1.10:3128",
              "https": "http://10.10.1.10:1080",
            }
        """
        try:
            socket.setdefaulttimeout(5)
            req = requests.get(url, proxies=proxy_dict)
            reponse_text = req.content.decode("utf-8")  
            
        except urllib2.HTTPError as ex :             
            print "Test Proxy access [error]: %s" % ex    
            return False   
        except Exception, info: #IndexError
            print "Test Proxy access [error]: %s" % info    
            return False

        return (reponse_text.find(verifytext) != -1)
    
    @staticmethod
    def GetFreeProxylist():  
        #socket.setdefaulttimeout(20)
        
        url="http://pachong.org/"
        proxyPagecontent = HttpGetwithJsExecuted(url)

        #proxyPagecontent = requests.get(url).content.decode("utf-8")
        if proxyPagecontent is None:  
            return  
        
        sel = Selector(None, proxyPagecontent.replace('\t','').replace('\r','').replace('\n',''), 'html')
        rows = sel.xpath('//tr[@data-id]')
            
        proxy_list = []
        for row in rows:
            ip = row.xpath('td[2]/text()').extract()[0]
            port = row.xpath('td[3]/text()').extract()[0]
            ip_port = "http://%s:%s" % (ip, port)
            proxy = { "http" : ip_port }
            if proxyfactory.__testproxy(proxy_dict=proxy):
                proxy_list.append(proxy)
                
        return proxy_list
                  
                  
if __name__ == "__main__":  
    proxy_list = proxyfactory.GetFreeProxylist()
    print proxy_list