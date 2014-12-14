# -*- coding: utf-8 -*-
# ref:
# http://www.wieschoo.com/tutorials/botsuite/captcha-ocr-tutorial-neural-network/00746/
# http://weijr-note.blogspot.tw/2012/11/python.html
# http://opencv-python-tutroals.readthedocs.org/en/latest/index.html
import cv2
import cv
import numpy as np
import pytesser
import random
import json
from collections import defaultdict

__all__ = ['TwseHisTraderCaptcha0', 'TwseHisTraderCaptcha1']

class TwseHisTraderCaptcha0(object):
    def __init__(self, debug=False):
        self._debug = debug

    def run(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #gray = cv2.equalizeHist(gray)
        #h, w = gray.shape
        # smooth backgroun noise
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        # threshold filter
        ret,th1 = cv2.threshold(blur, 220, 255, cv2.THRESH_BINARY)
        if self._debug:
            cv2.imshow('rule0', th1)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        text = pytesser.iplimage_to_string(cv.fromarray(th1), 'eng').strip()
        return text if text else ''


class TwseHisTraderCaptcha1(object):
    def __init__(self, debug=False):
        self._debug = debug

    def run(self, img):
        text = ''
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # resize as zoom in
        h, w = gray.shape
        #gray = cv2.pyrUp(gray)
        gray = cv2.resize(gray, (w*2, h*2), interpolation=cv2.INTER_CUBIC)
        # smooth background noise
        #gray = cv2.equalizeHist(gray)
        blur = cv2.GaussianBlur(gray, (7,7), 0)
        # threshold filter
        ret,th1 = cv2.threshold(blur, 240, 255, cv2.THRESH_BINARY)
        th2 = th1.copy()
        # find best match captcha area
        contours,hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        area = lambda (x, y, w, h): (w*h, x, y, w, h)
        best = sorted([area(cv2.boundingRect(cnt)) for cnt in contours], reverse=True)
        kernel = np.ones((1,1), np.uint8)
        # iter sub captcha
        for it in sorted(best[:5], key=lambda x: x[1]):
            th3 = th2[it[2]:it[2]+it[4], it[1]:it[1]+it[3]]
            # closing/opening
            open = cv2.morphologyEx(th3, cv2.MORPH_OPEN, kernel, iterations=5)
            close = cv2.morphologyEx(open, cv2.MORPH_CLOSE, kernel, iterations=5)
            mask = cv2.bitwise_and(th3, th3, mask=close)
            # regular size

            text += pytesser.iplimage_to_string(cv.fromarray(mask), 'eng', 10).strip()
        if self._debug:
            for it in sorted(best[:5], key=lambda x: x[1]):
                cv2.rectangle(th2, (it[1],it[2]), (it[1]+it[3],it[2]+it[4]), (255,255,255), 2)
            cv2.imshow('rule1', th2)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return text if text else ''


def test_captcha():
    exp = ['HKYAX', 'YK2F1', 'EVAH8']
    record = defaultdict(list)
    tests = [
        TwseHisTraderCaptcha0(debug=True),
        TwseHisTraderCaptcha1(debug=True),
    ]
    for test in tests:
        cnt = 0
        for i,it in enumerate(exp):
            img = cv2.imread("./train/twse_test%d.jpeg" %(i))
            cnt = cnt + 1 if test.run(img) == exp[i] else cnt
        record[cnt].append((test.__class__.__name__))
    print json.dumps(record, sort_keys=True, indent=4, separators=(',', ': '))

def main():
    test_captcha()

if __name__ == '__main__':
    main()
