# -*- coding: utf-8 -*-
# ref:
# http://www.wieschoo.com/tutorials/botsuite/captcha-ocr-tutorial-neural-network/00746/
# http://weijr-note.blogspot.tw/2012/11/python.html
# http://opencv-python-tutroals.readthedocs.org/en/latest/index.html
import cv2
import cv
import numpy as np
import pandas as pd
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
import tt
import traceback

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
            response = opener.open(self._domain + URL)
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
            return img
        except Exception:
            print 'error read captch img'
            pass

    def _predict_captcha(self, rule, loop=1):
        record = []
        try:
            url = self._find_captcha_path()
            for i in xrange(loop):
                img = self._read_captcha_img(url)
                text = tt.run(img)
#                text = raw_input('debug captcha:')
                if len(text) == 5:
                    record.append(text)
                time.sleep(2)
        except Exception:
            pass
        return Counter(record).most_common(1)[0][0] if record else ''

    def _download_csv(self, rule, stockid):
        try:
            self._form.update({
                'stk_code': stockid,
                'auth_num': self._predict_captcha(rule)
            })
            #print json.dumps(self._form, sort_keys=True, indent=4, separators=(',', ': '))
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cj))
            data = urllib.urlencode(self._form)
            URL = '/web/stock/aftertrading/broker_trading/brokerBS.php?l=zh-tw'
            response = opener.open(self._domain + URL)
            yy, mm, dd = map(int, datetime.tcnow().strftime('%Y-%m-%d').split('-'))
            yy = yy - 1911
            URL = (
                '/web/stock/aftertrading/broker_trading/download_ALLCSV.php?' +
                'curstk=%(stk)s&stk_date=%(date)s&auth=%(auth)s' ) % {
                    'stk': self._form['stk_code'],
                    'date': '%yy%mm%dd' %(yy, mm, dd),
                    'auth': self._form['auth_num']
            }
            response = opener.open(self._domain + URL)
            frame = pd.read_csv(
                StringIO(response.read()), delimiter=',',
                na_values=['--'], header=None, skiprows=[0, 1, 2], encoding=None, dtype=np.object)
            if len(frame.index) > 1:
                return True
        except Exception:
            print 'error download csv'
            pass
        return False

    def fetch_trader_info(self, rule, stockid, loop=0, max_loop=100):
        if max_loop > 0:
            if self._download_csv(rule, stockid):
                return loop
            else:
                time.sleep(2)
                self.fetch_trader_info(rule, stockid, loop+1, max_loop-1)

def test_captcha():
    cap = TestOtcHisTraderCaptcha()
    record = defaultdict(list)
    tests = [
        OtcHisTraderCaptcha0(),
        OtcHisTraderCaptcha1()
    ]
    for test in tests:
        runtime = cap.fetch_trader_info(test.run, '5371')
        if runtime:
            record[runtime].append((test.__class__.__name__))
    print json.dumps(record, sort_keys=True, indent=4, separators=(',', ': '))

def main():
    test_captcha()

if __name__ == '__main__':
    main()

