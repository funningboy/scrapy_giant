# -*- coding: utf-8 -*-
# ref:
# http://www.wieschoo.com/tutorials/botsuite/captcha-ocr-tutorial-neural-network/00746/
# http://weijr-note.blogspot.tw/2012/11/python.html
# http://opencv-python-tutroals.readthedocs.org/en/latest/index.html
import cv2
import cv
import numpy as np
import pytesser
import urllib2
import urllib
from lxml import etree
from StringIO import StringIO
from collections import Counter
import json
import cookielib
import time
from collections import defaultdict
from crawler.spiders.otchistrader_captcha import OtcHisTraderCaptcha0, OtcHisTraderCaptcha1

class TestOtcHisTraderCaptcha(object):

    def __init__(self):
        self._domain = ''
        self._cj = cookielib.CookieJar()


