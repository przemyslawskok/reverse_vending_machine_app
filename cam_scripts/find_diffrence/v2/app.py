#program which will load the static image and find the diffrance between the static image and the live image

import cv2


background = cv2.imread('static.jpg')


# capture frames from a camera
cap = cv2.VideoCapture(0)

while True:
    ret, live_img = cap.read()
    cv2.imshow('Actual frame', live_img)

    difference = cv2.subtract(background, live_img)
   
    Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
    difference[mask != 255] = [0, 0, 255]

    cv2.imshow('diffrence', difference)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


# img2 = Image.open('live.jpg')

# diff = ImageChops.difference(img1, img2)







diff.show()