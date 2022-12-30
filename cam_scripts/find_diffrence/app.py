#program which will load the static image and find the diffrance between the static image and the live image

import cv2

# import module
from PIL import Image, ImageChops

background = Image.open('static.jpg')


# capture frames from a camera
cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    cv2.imshow('Actual frame', img)
    #convert img to file 
    cv2.imwrite('live.jpg', img)
    live_image = Image.open('live.jpg')

    diff = ImageChops.difference(background, live_image)

    #save the diffrence image
    diff.save('diff.jpg')
    #load the diffrence image and shwo it
    diff = cv2.imread('diff.jpg')
    cv2.imshow('diffrence', diff)

    # Display the resulting frame
    #cv2.imshow('frame', diff)

    # Wait for Esc key to stop
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


# img2 = Image.open('live.jpg')

# diff = ImageChops.difference(img1, img2)







diff.show()