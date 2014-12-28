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
        img = cv2.cvtColor(img,cv2.CV_32F)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
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
                cv2.line(th0,(x1,y1),(x2,y2),(255,255,255),10)
        # smooth backgroun noise
        blur = cv2.GaussianBlur(th0, (5,5), 0)
        # threshold filter
        ret,th1 = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)
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
                cv2.imshow('rule1', mask)
                #cv2.imwrite('tt.png', mask)
                cv2.waitKey(0)
                cv2.destroyAllWindows()


class OtcHisTraderCaptcha1(object):
    def __init__(self, debug=False):
        self._debug = debug

    def run(self, img):

        def normalize(img):
            img = cv2.cvtColor(img, cv2.CV_32F)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            gray = cv2.equalizeHist(gray)
            ret,th0 = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            return th0

        def debug(img):
            cv2.imshow('test', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        def resize(img, resize=2):
            h,w = img.shape
            img = cv2.resize(img, (w*resize,h*resize), interpolation=cv2.INTER_CUBIC)
            return img

        def iter(img, it=5):
            h,w = img.shape
            return [img[:,iw:iw+w//it] for iw in xrange(0, w, w//it)]

        def preload_char(ttf="./train/font/BOLD.ttf", char="D", size=68):
            font = ImageFont.truetype(ttf,size)
            img = Image.new("RGBA", (200,200),(255,255,255))
            draw = ImageDraw.Draw(img)
            draw.text((0,0),char,(0,0,0),font=font)
            img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2GRAY)
            return img

        def boundary(img):
            # find best match captcha area
            edges = cv2.Canny(img, 150, 250, apertureSize=3)
            contours,hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            area = lambda (x, y, w, h): (w*h, x, y, w, h)
            b = sorted([area(cv2.boundingRect(cnt)) for cnt in contours], reverse=True)[0]
            img = img[b[2]:b[2]+b[4], b[1]:b[1]+b[3]]
            #debug(img)
            return img

        def target(ch, cap):
            c = zip(ch.shape, cap.shape)
            h,w = min(c[0]), min(c[1])
            ch = cv2.resize(ch, (w,h), interpolation=cv2.INTER_CUBIC)
            return ch

        def preload_captcha(cap="./train/otc_test2.png"):
            return normalize(cv2.imread(cap))

        def find_best_match(cap):
            chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            record = defaultdict(list)
            for char in chars:
                ch = target(boundary(preload_char(char=char)), cap)
                result = cv2.matchTemplate(ch, cap, cv2.TM_SQDIFF)
                r = result.min()
                c = np.unravel_index(result.argmin(), result.shape)
                pt2 = (c[1]+ch.shape[1], c[0]+ch.shape[0])
                record[r].append((char, c[::-1], pt2))

            k = sorted(record)[0]
            item = record[k][0]
            return item[0][0]

        text = ''
        for cap in iter(resize(preload_captcha(img=img))):
            text += find_best_match(cap)
        return text

def test_captcha():
    exp = ['AFDXF', 'I9L6D', '5HLUY']
    record = defaultdict(list)
    tests = [
        OtcHisTraderCaptcha0(debug=True),
        OtcHisTraderCaptcha1(debug=True),
    ]
    for test in tests:
        cnt = 0
        for i,it in enumerate(exp):
            img = cv2.imread("./train/otc_test%d.png" %(i))
            cnt = cnt + 1 if test.run(img) == exp[i] else cnt
        record[cnt].append((test.__class__.__name__))
    print json.dumps(record, sort_keys=True, indent=4, separators=(',', ': '))

def main():
    test_captcha()

if __name__ == '__main__':
    main()
