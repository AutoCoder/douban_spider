# Scrapy settings for douban project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os

BasicDir = os.path.dirname(__file__)
ProjectDir = os.path.dirname(BasicDir)

BOT_NAME = 'douban'

SPIDER_MODULES = ['douban.spiders']
NEWSPIDER_MODULE = 'douban.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'douban (+http://www.yourdomain.com)'
ITEM_PIPELINES = {'douban.pipelines.DoubanPreprocessPipeline': 1,
                  'douban.pipelines.DoubanStore2DbPipeline': 2
                  }

DOWNLOAD_DELAY = 2

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'douban.middlewares.ProxyMiddleware': 100,
}
