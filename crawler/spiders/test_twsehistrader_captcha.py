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
from crawler.spiders.twsehistrader_captcha import TwseHisTraderCaptcha0, TwseHisTraderCaptcha1


class TestTwseHisTraderCaptcha(object):

    def __init__(self):
        self._domain = 'http://bsr.twse.com.tw'
        self._form = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': '',
            '__EVENTVALIDATION': '',
            'RadioButton_Normal': 'RadioButton_Normal',
            'TextBox_Stkno': '',
            'CaptchaControl1': '',
            'btnOK': u'查詢'.encode('utf-8')
        }
        self._cj = cookielib.CookieJar()

    def _find_captcha_path(self):
        try:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cj))
            response = opener.open(self._domain + '/bshtm/bsMenu.aspx')
            root = etree.parse(StringIO(response.read()), etree.HTMLParser())
            self._form.update({
                '__VIEWSTATE': root.xpath('.//input[@id="__VIEWSTATE"]/@value')[0],
                '__EVENTVALIDATION': root.xpath('.//input[@id="__EVENTVALIDATION"]/@value')[0]
            })
            return self._domain + '/bshtm/' + root.xpath('.//td/div/div/img/@src')[0]
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

    def _predict_captcha(self, rule, loop=3):
        record = []
        try:
            url = self._find_captcha_path()
            for i in xrange(loop):
                img = self._read_captcha_img(url)
                text = rule(img)
                print text
                if len(text) == 5:
                    record.append(text)
                time.sleep(2)
        except Exception:
            pass
        return Counter(record).most_common(1)[0][0] if record else ''

    def _download_csv(self, rule, stockid):
        try:
            self._form.update({
                'TextBox_Stkno': stockid,
                'CaptchaControl1': self._predict_captcha(rule)
            })
            #print json.dumps(self._form, sort_keys=True, indent=4, separators=(',', ': '))
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cj))
            data = urllib.urlencode(self._form)
            response = opener.open(self._domain + '/bshtm/bsMenu.aspx', data)
            root = etree.parse(StringIO(response.read()), etree.HTMLParser())
            find = root.xpath('.//a[@id="HyperLink_DownloadCSV"]/@href')
            if find:
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cj))
                response = opener.open(self._domain + '/bshtm/' + find[0])
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
                return self.fetch_trader_info(rule, stockid, loop+1, max_loop-1)

def test_captcha():
    cap = TestTwseHisTraderCaptcha()
    record = defaultdict(list)
    tests = [
        TwseHisTraderCaptcha0(),
        TwseHisTraderCaptcha1()
    ]
    for test in tests:
        print test.__class__.__name__
        runtime = cap.fetch_trader_info(test.run, '2317')
        if runtime:
            record[runtime].append((test.__class__.__name__))
    print json.dumps(record, sort_keys=True, indent=4, separators=(',', ': '))

def main():
    test_captcha()

if __name__ == '__main__':
    main()
