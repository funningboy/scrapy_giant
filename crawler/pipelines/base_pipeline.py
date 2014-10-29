# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
from bson import json_util
# not work for scrapy
# from gevent import monkey; monkey.patch_all()

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from bin.mongodb_driver import *

__all__ = ['BasePipeline']

class BasePipeline(object):
    def __init__(self):
        # ref http://stackoverflow.com/questions/4113275/scrapy-pipeline-spider-opened-and-spider-closed-not-being-called
        self._name = None
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):
        if spider.name not in [self._name]:
            return

    def _encode_item(self, item):
        # encode item as json stream
        return json.dumps(dict(item), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)

    def _decode_item(self, stream):
        # decode json stream as dict item
        return json.loads(stream, encoding='utf-8')

    def process_item(self, item, spider):
        if spider.name not in [self._name]:
            return item

    def spider_closed(self, spider):
        if spider.name not in [self._name]:
            return
