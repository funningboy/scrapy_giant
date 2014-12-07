# -*- coding: utf-8 -*-

import cv2
import cv
import numpy as np
from matplotlib import pyplot as plt
from handler import pytesser
import urllib2
import urllib
from lxml import etree
from StringIO import StringIO
from collections import Counter
import json
import cookielib
import time

domain = 'http://bsr.twse.com.tw'

form = {
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

cj = cookielib.CookieJar()

def find_captcha_path():
    global domain, form, cj
    try:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        response = opener.open(domain + '/bshtm/bsMenu.aspx')
        root = etree.parse(StringIO(response.read()), etree.HTMLParser())
        form.update({
            '__VIEWSTATE': root.xpath('.//input[@id="__VIEWSTATE"]/@value')[0],
            '__EVENTVALIDATION': root.xpath('.//input[@id="__EVENTVALIDATION"]/@value')[0]
        })
        return domain + '/bshtm/' + root.xpath('.//td/div/div/img/@src')[0]
    except Exception:
        pass

def read_captcha_img(url):
    global cj
    try:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        response = opener.open(url)
        arr = np.asarray(bytearray(response.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1) # 'load it as it is'
        #cv2.imwrite('tt.jpeg', img)
        return img
    except Exception:
        pass

def try_predict_captcha(rule, loop=1):
    record = []
    url = find_captcha_path()
    for i in xrange(loop):
        try:
            img = read_captcha_img(url)
            text = rule(img).strip()
            if len(text) == 5:
                record.append(text)
            time.sleep(0.5)
        except Exception:
            time.sleep(2)
            pass
    return Counter(record).most_common(1)[0][0] if record else ""

def run_pytesser_rule1(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # smooth noise to background
    blur = cv2.GaussianBlur(gray,(5,5),0)
    # threshold filter
    ret,th1 = cv2.threshold(blur,223,255,cv2.THRESH_BINARY)
    return pytesser.iplimage_to_string(cv.fromarray(th1))

def run_pytesser_rule2(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # smooth noise to background
    blur = cv2.GaussianBlur(gray,(5,5),0)
    # threshold filter
    ret,th1 = cv2.threshold(blur,223,255,cv2.THRESH_BINARY)
    return pytesser.iplimage_to_string(cv.fromarray(th1))

def fetch_trader_info(rule, stockid, max_loop=20):
    global form, cj, domain
    loop = 0;
    while loop < max_loop:
        captcha = try_predict_captcha(rule)
        form.update({
            'TextBox_Stkno': stockid,
            'CaptchaControl1': captcha
        })
        #print json.dumps(form, sort_keys=True, indent=4, separators=(',', ': '))

        try:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            data = urllib.urlencode(form)
            response = opener.open(domain + '/bshtm/bsMenu.aspx', data)
            root = etree.parse(StringIO(response.read()), etree.HTMLParser())
            find = root.xpath('.//a[@id="HyperLink_DownloadCSV"]/@href')
            if find:
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                response = opener.open(domain + '/bshtm/' + find[0])
                return loop
            else:
                loop += 1
            time.sleep(0.5)
        except Exception:
            time.sleep(2)
            pass

def main():
    pytesser_rules = [
        run_pytesser_rule1,
        run_pytesser_rule2
    ]
    record = {}
    stockids = ['2317', '2330', '1314']
    for it in xrange(10000):
        for rule in pytesser_rules:
            for stockid in stockids:
                record.update({
                    stockid: fetch_trader_info(rule, stockid)
                })
        print record

if __name__ == '__main__':
    main()
