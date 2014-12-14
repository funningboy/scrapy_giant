

__all__ = ['TwseCaptchaHandler', 'OtcCaptchaHandler']

class TwseCaptchaHandler(object):

class CaptchaRule0(BaseRule):
    def __init__(self, rand=False, debug=False):
        super(CaptchaRule0, self).__init__(rand, debug)
        self._cfg = {
            0: {
                'GAUSSIANBLUR': tuple([random.randrange(1, 7, 2)]*2) if rand else (5,5)
            },
            1: {
                'THRESHOLD': random.randint(200, 250) if rand else 225
            }
        }

    def run(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #gray = cv2.equalizeHist(gray)
        #h, w = gray.shape
        # smooth backgroun noised
        blur = cv2.GaussianBlur(gray, self._cfg[0]['GAUSSIANBLUR'], 0)
        # threshold filter
        ret,th1 = cv2.threshold(blur, self._cfg[1]['THRESHOLD'], 255, cv2.THRESH_BINARY)
        if self._debug:
            cv2.imshow('rule0', th1)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        text = pytesser.iplimage_to_string(cv.fromarray(th1), 'eng').strip()
        return text if text else ''

class CaptchaRule1(BaseRule):
    def __init__(self, rand=False, debug=False):
        super(CaptchaRule1, self).__init__(rand, debug)
        self._cfg = {
            0: {
                'GAUSSIANBLUR': tuple([random.randrange(3, 9, 2)]*2) if rand else (7,7)
            },
            1: {
                'THRESHOLD': random.randint(200, 250) if rand else 240
            },
            2: {
                'KERNEL': tuple([random.randrange(1, 7, 2)]*2) if rand else (1,1)
            }
        }

    def run(self, img):
        text = ''
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # resize as zoom in
        h, w = gray.shape
        #gray = cv2.pyrUp(gray)
        gray = cv2.resize(gray, (w*2, h*2), interpolation=cv2.INTER_CUBIC)
        # smooth background noise
        #gray = cv2.equalizeHist(gray)
        blur = cv2.GaussianBlur(gray, self._cfg[0]['GAUSSIANBLUR'], 0)
        # threshold filter
        ret,th1 = cv2.threshold(blur, self._cfg[1]['THRESHOLD'], 255, cv2.THRESH_BINARY)
        th2 = th1.copy()
        # find best match captcha area
        contours,hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        area = lambda (x, y, w, h): (w*h, x, y, w, h)
        best = sorted([area(cv2.boundingRect(cnt)) for cnt in contours], reverse=True)[:5]
        kernel = np.ones(self._cfg[2]['KERNEL'], np.uint8)
        # iter sub captcha
        for it in sorted(best, key=lambda x: x[1]):
            th3 = th2[it[2]-2:it[2]+it[4]+2, it[1]-2:it[1]+it[3]+2]
            # closing/opening
            open = cv2.morphologyEx(th3, cv2.MORPH_OPEN, kernel, iterations=5)
            close = cv2.morphologyEx(open, cv2.MORPH_CLOSE, kernel, iterations=5)
            mask = cv2.bitwise_and(th3, th3, mask=close)
            text += pytesser.iplimage_to_string(cv.fromarray(mask), 'eng', 10).strip()
        if self._debug:
            for it in sorted(best, key=lambda x: x[1]):
                cv2.rectangle(th2, (it[1]-2,it[2]-2), (it[1]+it[3]+2,it[2]+it[4]+2), (255,255,255), 2)
            cv2.imshow('rule1', th2)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return text if text else ''

class CaptchaRule2(object):
    def __init__(self, rand=False, debug=False):
        pass


