# -*- coding: utf-8 -*-
# only run for warrant
import cv2
import cv
import numpy as np
import pytesser
import random
import json
from collections import defaultdict
from PIL import ImageFont, ImageDraw, Image

__all__ = ['OtcHisTraderCaptcha0', 'OtcHisTraderCaptcha1']

class OtcHisTraderCaptcha0(object):
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

        def filter(img):
            edges = cv2.Canny(img, 150, 250, apertureSize=3)
            lines = cv2.HoughLinesP(edges,1,np.pi/180, 1, 3, 1)
            # remove boundary as white line
            for line in lines:
                for x1,y1,x2,y2 in line:
                    cv2.line(img,(x1,y1),(x2,y2),(255,255,255),14)
            # smooth background noise
            blur = cv2.GaussianBlur(img, (5,5), 0)
            # threshold filter
            ret,th1 = cv2.threshold(blur, 250, 255, cv2.THRESH_BINARY)
            return th1

        def extend(img, ext=30):
            h, w = img.shape
            wtimg = 255 - normalize(np.zeros((h+ext,w,3), np.uint8))
            wtimg[(h+ext)//2-h//2:(h+ext)//2+h//2,:w] = img[:h,:w]
            return wtimg

        def boundary(img, bund=-1):
            # find best match captcha area
            contours,hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            area = lambda (x, y, w, h): (w*h, x, y, w, h)
            best = sorted([area(cv2.boundingRect(cnt)) for cnt in contours], reverse=True)
            # iter sub captcha
            x0 = lambda x: x-bund if x > bund else 0
            y0 = lambda y: y-bund if y > bund else 0
            x1 = lambda x: x+bund if w-bund > x else w
            y1 = lambda y: y+bund if h-bund > y else h
            for it in sorted(best[1:6], key=lambda x: x[1]):
                yield ((x0(it[1]),y0(it[2])), (x1(it[1]+it[3]),y1(it[2]+it[4])))

        def feature(img):
            kernel = np.ones((1,1), np.uint8)
            # smooth backgroun noise
            blur = cv2.GaussianBlur(img, (5,5), 0)
            # threshold filter
            ret,th1 = cv2.threshold(blur, 235, 255, cv2.THRESH_BINARY)
            # colsing/opening
            open = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel, iterations=5)
            close = cv2.morphologyEx(open, cv2.MORPH_CLOSE, kernel, iterations=5)
            mask = cv2.bitwise_and(th1, th1, mask=close)
            return mask

        def debug(img, bund):
            cv2.rectangle(img, bund[0], bund[1], (0,0,0), 1)
            cv2.imshow('test', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        text = ''
        img = extend(resize(normalize(img), 4))
        h, w = img.shape
        bkimg = np.zeros((h,w,3), np.uint8)
        bkimg = 255 - resize(normalize(bkimg), 1)
        for bund in boundary(filter(img.copy()), -7):
            x,y = zip(*bund)
            bkimg[y[0]:y[1],x[0]:x[1]] = img[y[0]:y[1],x[0]:x[1]]
            if self._debug:
                debug(bkimg, bund)
        text = pytesser.iplimage_to_string(cv.fromarray(bkimg), 'eng').strip()
        return text if text else ''


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

        def resize(img, resize=2):
            h,w = img.shape
            img = cv2.resize(img, (w*resize,h*resize), interpolation=cv2.INTER_CUBIC)
            return img

        def iter(img, it=5):
            h,w = img.shape
            return [img[:,iw:iw+w//it] for iw in xrange(0, w, w//it)]

        def preload_char(ttf="./crawler/spiders/train/font/BOLD.ttf", char="D", size=68):
            font = ImageFont.truetype(ttf,size)
            img = Image.new("RGBA", (200,200),(255,255,255))
            draw = ImageDraw.Draw(img)
            draw.text((0,0),char,(0,0,0),font=font)
            img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2GRAY)
            return img

        def boundary(img, bund=3):
            # find best match captcha area
            edges = cv2.Canny(img, 150, 250, apertureSize=3)
            contours,hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            area = lambda (x, y, w, h): (w*h, x, y, w, h)
            b = sorted([area(cv2.boundingRect(cnt)) for cnt in contours], reverse=True)[0]
            img = img[b[2]:b[2]+b[4], b[1]:b[1]+b[3]]
            return img

        def target(ch, cap):
            c = zip(ch.shape, cap.shape)
            h,w = min(c[0]), min(c[1])
            ch = cv2.resize(ch, (w,h), interpolation=cv2.INTER_CUBIC)
            return ch

        def debug(img):
            cv2.imshow('test', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

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
        for cap in iter(resize(normalize(img))):
            text += find_best_match(cap)
        if self._debug:
            debug(img)
        return text

def test_captcha():
    exp = ['AFDXF', 'I9L6D', '5HLUY']
    record = defaultdict(list)
    tests = [
#        OtcHisTraderCaptcha0(debug=True),
        OtcHisTraderCaptcha1(debug=True),
    ]
    for test in tests:
        cnt = 0
        for i,it in enumerate(exp):
            img = cv2.imread("./crawler/spiders/train/otc_test%d.png" %(i))
            cnt = cnt + 1 if test.run(img) == exp[i] else cnt
        record[cnt].append((test.__class__.__name__))
    print json.dumps(record, sort_keys=True, indent=4, separators=(',', ': '))

def main():
    test_captcha()

if __name__ == '__main__':
    main()
