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

        def normalize(img):
            img = cv2.cvtColor(img, cv2.CV_32F)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            gray = cv2.equalizeHist(gray)
            ret,th0 = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            return th0

        def resize(img, resize=2):
            h,w = img.shape
            img = cv2.resize(img, (w*resize,h*resize), interpolation=cv2.INTER_CUBIC)
            return img

        def feature(img):
            # smooth backgroun noise
            blur = cv2.GaussianBlur(gray, (5,5), 0)
            # threshold filter
            ret,th1 = cv2.threshold(blur, 220, 255, cv2.THRESH_BINARY)
            # colsing/opening
            open = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel, iterations=5)
            close = cv2.morphologyEx(open, cv2.MORPH_CLOSE, kernel, iterations=5)
            mask = cv2.bitwise_and(th1, th1, mask=close)
            return mask

        def debug(img):
            cv2.imshow('test', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        img = feature(resize(normalize(img)))
        if self._debug:
            debug(img)
        text = pytesser.iplimage_to_string(cv.fromarray(img), 'eng').strip()
        return text if text else ''


class TwseHisTraderCaptcha1(object):
    def __init__(self, debug=False):
        self._debug = debug

    def run(self, img):

        def normalize(img):
            img = cv2.cvtColor(img, cv2.CV_32F)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            gray = cv2.equalizeHist(gray)
            ret,th0 = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            return th0

        def resize(img, resize=2):
            h,w = img.shape
            img = cv2.resize(img, (w*resize,h*resize), interpolation=cv2.INTER_CUBIC)
            return img

        def feature(img):
            h, w = img.shape
            # find best match captcha area
            contours,hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            area = lambda (x, y, w, h): (w*h, x, y, w, h)
            best = sorted([area(cv2.boundingRect(cnt)) for cnt in contours], reverse=True)
            kernel = np.ones((1,1), np.uint8)
            # iter sub captcha
            for it in sorted(best[:5], key=lambda x: x[1]):
                ft = img[it[2]:it[2]+it[4], it[1]:it[1]+it[3]]
                # closing/opening
                open = cv2.morphologyEx(ft, cv2.MORPH_OPEN, kernel, iterations=5)
                close = cv2.morphologyEx(open, cv2.MORPH_CLOSE, kernel, iterations=5)
                mask = cv2.bitwise_and(ft, ft, mask=close)
                yield mask

        def debug(img):
            cv2.imshow('test', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        text = ''
        for it in feature(resize(normalize(img))):
            text += pytesser.iplimage_to_string(cv.fromarray(it), 'eng', 10).strip()
            if self._debug:
                debug(img)
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
