# -*- coding: utf-8 -*-

import pandas as pd
import pytz
from collections import OrderedDict
from bson import json_util

from mongoengine import *
from bin.start import switch
from bin.mongodb_driver import MongoDBDriver

__all__ ['']

#class SuperManHandler():
#
#    def __init__(self):
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('twsehisdb', host=host, port=port, alias='twsehisdb')
        twsehiscoll = switch(TwseHisColl, 'twsehisdb')
        self._stock = TwseStockHisDBHandler(twsehiscoll)
        self._trader = TwseTraderHisDBHandler(twsehiscoll)
#
#class ZombieHandler():
#
#    def __init__(self):

class
