# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TwseHisTraderItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    date = scrapy.Field()
    stockid = scrapy.Field()
    stocknm = scrapy.Field()
    count = scrapy.Field()
    open = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    close = scrapy.Field()
    volume = scrapy.Field()
    traderlist = scrapy.Field()
#    traderlist: [{
#       index = scrapy.Field()
#       traderid = scrapy.Field()
#       tradernm = scrapy.Field()
#       price = scrapy.Field()
#       buyvolume = scrapy.Field()
#       sellvolume = scrapy.Field()
#    }...]
    toplist = scrapy.Field()

class TwseIdItem(scrapy.Item):
    data = scrapy.Field()
# data:[{
#    stockid = scrapy.Field()
#    stocknm = scrapy.Field()
#    onmarket = scrapy.Field()
#    industry = scrapy.Field()
#  }...]

class TwseHisStockItem(scrapy.Item):
    url = scrapy.Field()
    stockid = scrapy.Field()
    stocknm = scrapy.Field()
    count = scrapy.Field()
    data = scrapy.Field()
#   data:[{
#       date = scrapy.Field()
#       exhvolume = scrapy.Field()
#       exhprice = scrapy.Field()
#       open = scrapy.Field()
#       high = scrapy.Field()
#       low = scrapy.Field()
#       close = scrapy.Field()
#       offset = scrapy.Field()
#       volume = scrapy.Field()
#       }, ...
#   ]

class TwseRelStockItem(scrapy.Item):
    url = scrapy.Field()
    stockid = scrapy.Field()
    stocknm = scrapy.Field()
    count = scrapy.Field()
    data = scrapy.Field()
#   data:[{
#       date = scrapy.Field()
#       exhvolume = scrapy.Field()
#       exhprice = scrapy.Field()
#       open = scrapy.Field()
#       high = scrapy.Field()
#       low = scrapy.Field()
#       close = scrapy.Field()
#       offset = scrapy.Field()
#       volume = scrapy.Field()
#       }, ...
#   ]

class OtcHisTraderItem(TwseHisTraderItem):
    pass

class OtcHisStockItem(TwseHisStockItem):
    pass

class OtcIdItem(TwseIdItem):
    pass

class OtcRelStockItem(TwseRelStockItem):
    pass
