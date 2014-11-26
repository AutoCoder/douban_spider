'''
Created on 2014.11.17

@author: tj_liyuan
'''
from selenium import webdriver


def HttpGetwithJsExecuted(url):
    """
    To use PhantomJS in windows, you need install phantomjs.exe into path C:\Python27\Scripts
    """
    driver = webdriver.PhantomJS()
    driver.get(url)
    proxyPagecontent = driver.page_source
    driver.quit
    
    return proxyPagecontent
