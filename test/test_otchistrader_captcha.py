# -*- coding: utf-8 -*-
# ref:
# http://www.wieschoo.com/tutorials/botsuite/captcha-ocr-tutorial-neural-network/00746/
# http://weijr-note.blogspot.tw/2012/11/python.html
# http://opencv-python-tutroals.readthedocs.org/en/latest/index.html
import cv2
import cv
import numpy as np
import pandas as pd
import urllib2
import urllib
from lxml import etree
from StringIO import StringIO
from collections import Counter
import json
import cookielib
import time
from datetime import datetime
from collections import defaultdict
from crawler.spiders.otchistrader_captcha import OtcHisTraderCaptcha0, OtcHisTraderCaptcha1
from crawler.spiders.pytesser import *


class TestOtcHisTraderCaptcha(object):

    def __init__(self):
        self._domain = 'http://www.gretai.org.tw'
        self._form = {
            'stk_code': '',
            'auth_num': ''
        }
        self._cj = cookielib.CookieJar()

    def _find_captcha_path(self):
        try:
            URL = '/web/stock/aftertrading/broker_trading/brokerBS.php?l=zh-tw'
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cj))
            opener.addheaders = [
                ('User-Agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.11) Gecko/20101012 Firefox/3.6.11'),
            ]
            response = opener.open(self._domain + URL)
            print self._cj
            return self._domain + '/web/inc/authnum.php'
        except Exception:
            print 'error find captch path'
            pass

    def _read_captcha_img(self, url):
        try:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cj))
            response = opener.open(url)
            arr = np.asarray(bytearray(response.read()), dtype=np.uint8)
            img = cv2.imdecode(arr, -1)
            print self._cj
            return img
        except Exception:
            print 'error read captch img'
            pass

    def _predict_captcha(self, rule_cb, loop=1):
        record = []
        try:
            url = self._find_captcha_path()
            for i in xrange(loop):
                img = self._read_captcha_img(url)
                text = rule_cb(img)
                print text
                if len(text) == 5:
                    record.append(text)
                time.sleep(2)
        except Exception:
            print 'error predict captcha'
            pass
        return Counter(record).most_common(1)[0][0] if record else ''

    def _download_csv(self, rule_cb, stockid, debug=False):
        try:
            self._form.update({
                'stk_code': stockid,
                'auth_num': self._predict_captcha(rule_cb, 1)
            })
            if debug:
                self._form.update({
                    'auth_num': raw_input('debug:')
                })
            #print json.dumps(self._form, sort_keys=True, indent=4, separators=(',', ': '))
            print self._cj
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cj))
            data = urllib.urlencode(self._form)
            URL = '/web/stock/aftertrading/broker_trading/brokerBS.php?l=zh-tw'
            response = opener.open(self._domain + URL, data)
            root = etree.parse(StringIO(response.read()), etree.HTMLParser())
            find = root.xpath('/html/body/center/div[3]/div[2]/div[4]/div[2]/div[2]/button[1]/text()')
            print find
            if find:
                yy, mm, dd = map(int, datetime.utcnow().strftime('%Y-%m-%d').split('-'))
                yy = yy - 1911
                URL = (
                    '/web/stock/aftertrading/broker_trading/download_ALLCSV.php?' +
                    'curstk=%(stk)s&auth=%(auth)s') % {
                        'stk': self._form['stk_code'],
                        'auth': self._form['auth_num']
                }
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cj))
                response = opener.open(self._domain + URL)
                try:
                    frame = pd.read_csv(
                        StringIO(response.read()), delimiter=',',
                        na_values=['--'], header=None, skiprows=[0, 1, 2], encoding=None, dtype=np.object)
                    if frame.index > 1:
                        print frame
                        return True
                except:
                    pass
        except Exception:
            print 'error download csv'
            pass
        return False

    def fetch_trader_info(self, rule_cb, stockid, debug=False, loop=0, max_loop=100):
        if max_loop > 0:
            if self._download_csv(rule_cb, stockid, debug):
                return loop
            else:
                time.sleep(2)
                self.fetch_trader_info(rule_cb, stockid, debug, loop+1, max_loop-1)

def test_captcha(debug=False):
    cap = TestOtcHisTraderCaptcha()
    record = defaultdict(list)
    tests = [
#        OtcHisTraderCaptcha0(debug),
        OtcHisTraderCaptcha1(debug)
    ]
    for test in tests:
        print test.__class__.__name__
        runtime = cap.fetch_trader_info(test.run, '5371', debug)
        if runtime:
            record[runtime].append((test.__class__.__name__))
    print json.dumps(record, sort_keys=True, indent=4, separators=(',', ': '))

def main():
    test_captcha(True)

if __name__ == '__main__':
    main()

