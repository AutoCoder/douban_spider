#!/usr/bin/env python  
#encoding: utf-8  
  
import unittest
from douban.utility import Utility
from scrapy.selector import Selector

class doubantest(unittest.TestCase):  
      
    ##初始化工作  
    def setUp(self):  
        pass  
      
    #退出清理工作  
    def tearDown(self):  
        pass  
      
    #具体的测试用例，一定要以test开头  
    def testExtractZanCount(self):  
        self.assertEqual(Utility.ExtractNumInbracket("赞(10)"), '10', 'Utility.ExtractNumInbracket extract zan count fail')
        self.assertEqual(Utility.ExtractNumInbracket("zan(10)"), '10', 'Utility.ExtractNumInbracket extract zan count fail')
        self.assertEqual(Utility.ExtractNumInbracket("赞"), 0, 'Utility.ExtractNumInbracket extract zan count fail')
                         
    def testxpath(self):
        str = u"""<div class="operation_div" id="60967686">
            <div class="operation-more" style="display: none;">
                <a rel="nofollow" href="javascript:void(0);" data-cid="805350130" class="lnk-delete-comment" title="真的要删除陈先生的发言?">删除</a>
            </div>
            <a rel="nofollow" href="javascript:void(0);" class="comment-vote lnk-fav">赞 (3)</a>
            <a href="http://www.douban.com/group/topic/67512273/?cid=805350130#last" class="lnk-reply">回应</a>
        </div>"""
        sel = Selector(None, str, 'html')
        node = sel.xpath('//a[2]/text()')
        str_ret = ''.join(node.extract())
        self.assertEqual(Utility.ExtractNumInbracket(str_ret), '3', 'Utility.ExtractNumInbracket extract zan count fail')
        
if __name__ =='__main__':  
    unittest.main()  