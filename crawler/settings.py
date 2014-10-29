# -*- coding: utf-8 -*-

# Scrapy settings for giant project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

DOWNLOAD_DELAY = 0.25    # 250 ms of delay

## some sane limits by default (override if needed)
#CLOSESPIDER_PAGECOUNT = 1000
CLOSESPIDER_TIMEOUT = 3600
CLOSESPIDER_ERRORCOUNT = 100
#CLOSESPIDER_ITEMCOUNT = 100

CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8

RETRY_ENABLED = False
COOKIES_ENABLED = False

LOG_ENABLED = True
LOG_LEVEL = 'INFO'

# our ginat internal debug set
GIANT_DEBUG = False
GIANT_LIMIT = 0

ITEM_PIPELINES = {
    'crawler.pipelines.base_pipeline.BasePipeline': 800,
    # tesehis trader/stock
    'crawler.pipelines.twseid_pipeline.TwseIdPipeline': 800,
    'crawler.pipelines.twsehistrader_pipeline.TwseHisTraderPipeline': 800,
    'crawler.pipelines.twsehisstock_pipeline.TwseHisStockPipeline': 800,
    # otchis trader/stock
    'crawler.pipelines.otcid_pipeline.OtcIdPipeline': 800,
    'crawler.pipelines.otchistrader_pipeline.OtcHisTraderPipeline': 800,
    'crawler.pipelines.otchisstock_pipeline.OtcHisStockPipeline': 800
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'giant (+http://www.yourdomain.com)'
