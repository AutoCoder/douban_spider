'''
Created on 2014.11.17

@author: tj_liyuan
'''
import time
from datetime import datetime

class Utility(object):
    
    @staticmethod
    def Timestr2Timestamp(time_str, time_format = "%Y-%m-%d %H:%M:%S"):
        """return -1 if input is invalid"""
        if time_str and format:
            t = time.strptime(time_str, time_format)
            return int(time.mktime(t))
        else:
            return -1
        
    @staticmethod
    def Timestamp2Timestr(timestamp, time_format = "%Y-%m-%d %H:%M:%S"):
        """return -1 if input is invalid"""
        if timestamp and format:
            return datetime.fromtimestamp(timestamp).strftime(time_format)
        else:
            return None
    
    @staticmethod
    def TimeToNow(time_str="", time_format = "%Y-%m-%d %H:%M:%S"):
        datenow = datetime.now()
        dateinput = datetime.strptime(time_str, time_format)  
        return datenow - dateinput