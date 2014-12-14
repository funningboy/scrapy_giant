# -*- coding: utf-8 -*-

import cv2
import cv
import numpy as np
import pytesser
import random
import json
from collections import defaultdict

__all__ = ['OtcHisTraderCaptcha0', 'OtcHisTraderCaptcha1']

class OtcHisTraderCaptcha0(object):
    def __init__(self, debug=False):
        self._debug = debug

    def run(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret,th0 = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        # resize as zoom in
        h, w = th0.shape
        #gray = cv2.pyrUp(gray)
        th0 = cv2.resize(th0, (w*4, h*4), interpolation=cv2.INTER_CUBIC)
        edges = cv2.Canny(th0, 150, 250, apertureSize=3)
        lines = cv2.HoughLinesP(edges,1,np.pi/180, 1, 3, 1)
        # remove boundary
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(th0,(x1,y1),(x2,y2),(255,255,255),7)
#        # smooth backgroun noise
        blur = cv2.GaussianBlur(th0, (5,5), 0)
        # threshold filter
        ret,th1 = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)
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
        if self._debug:
            for it in sorted(best[:5], key=lambda x: x[1]):
                cv2.rectangle(th2, (it[1],it[2]), (it[1]+it[3],it[2]+it[4]), (0,0,0), 2)
            cv2.imshow('rule1', th2)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

def test_captcha():
    exp = ['K2PBW', 'UJ19P', '13ERW']
    record = defaultdict(list)
    tests = [
        OtcHisTraderCaptcha0(debug=True),
#        OtcHisTraderCaptcha1(debug=True),
    ]
    for test in tests:
        cnt = 0
        for i,it in enumerate(exp):
            img = cv2.imread("./train/otc_test%d.jpeg" %(i))
            cnt = cnt + 1 if test.run(img) == exp[i] else cnt
        record[cnt].append((test.__class__.__name__))
    print json.dumps(record, sort_keys=True, indent=4, separators=(',', ': '))

def main():
    test_captcha()

if __name__ == '__main__':
    main()
