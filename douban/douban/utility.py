'''
Created on 2014.11.17

@author: tj_liyuan
'''
import time

class Utility(object):
    
    @staticmethod
    def Timestr2Timestamp(time_str, format = "%Y-%m-%d %H:%M:%S"):
        """return -1 if input is invalid"""
        if time_str and format:
            t = time.strptime(time_str, format)
            return int(time.mktime(t))
        else:
            return -1