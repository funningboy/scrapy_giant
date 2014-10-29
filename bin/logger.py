# -*- coding: utf-8 -*-

import logging

Logger = logging.getLogger('giant_scrapy')
hdlr = logging.FileHandler('giant_scrapy.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
Logger.addHandler(hdlr)
