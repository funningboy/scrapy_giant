import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import cv2
import cv2.cv as cv
import numpy as np
from collections import defaultdict, OrderedDict

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
    return img

def target(ch, cap):
    c = zip(ch.shape, cap.shape)
    h,w = min(c[0]), min(c[1])
    ch = cv2.resize(ch, (w-2,h-2), interpolation=cv2.INTER_CUBIC)
    return ch

def preload_captcha(cap="./train/otc_test2.png", img=None):
    return normalize(img)

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
    print item
    return item[0][0]

def run(img=None):
    text = ''
    for cap in iter(resize(preload_captcha(img=img))):
        text += find_best_match(cap)
    return text

def main():
    run()

if __name__ == '__main__':
    main()
