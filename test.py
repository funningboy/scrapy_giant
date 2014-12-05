import pytesseract
import Image
import cv2
import cv
from matplotlib import pyplot as plt

img = cv2.imread('test.jpeg')
blur = cv2.blur(img, (5,5))
#cv2.guassion

ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
ret,thresh3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
ret,thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
ret,thresh5 = cv2.threshold(img,200,255,cv2.THRESH_TOZERO_INV)

thresh = ['img','thresh1','thresh2','thresh3','thresh4','thresh5']

for i in xrange(6):
#    plt.subplot(2,3,i+1),plt.imshow(eval(thresh[i]),'gray')
#    plt.title(thresh[i])
#    plt.show()
    cv2.imwrite("i-%d.png" %(i), eval(thresh[i]))
    
for i in xrange(6): 
    print pytesseract.image_to_string(Image.open("i-%d.png" %(i)))
#cv2.imwrite("1.jpeg" %(i), blur)
#    cv2.imshow('Blur',blur)
#    cv2.waitKey(DELAY_BLUR)
#    pytesseract.image_to_string(Image.open('test2.jpeg'))
