import cv2
from PIL import Image, ImageChops
background = Image.open('static.jpg')
cap = cv2.VideoCapture(0)
while True:
    #check if clicked r
    
    ret, img = cap.read()


    if cv2.waitKey(1) & 0xFF == ord('r'):
        #save image as background
        cv2.imwrite('static.jpg', img)
        background = Image.open('static.jpg')
        print('background saved')



    cv2.imshow('Actual frame', img)
    cv2.imwrite('live.jpg', img)
    live_image = Image.open('live.jpg')
    diff = ImageChops.difference(background, live_image)
    diff.save('diff.jpg')
    diff = cv2.imread('diff.jpg')
    cv2.imshow('diffrence before gray', diff)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    cv2.imshow('diffrence after gray', diff_gray)
    #treshhold
    ret, diff_gray = cv2.threshold(diff_gray, 40, 255, cv2.THRESH_BINARY)
    cv2.imshow('diffrence after treshhold', diff_gray)

    #find contours
    contours, hierarchy = cv2.findContours(diff_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(diff, contours, -1, (0, 0, 255), 3)
    cv2.imshow('diffrence after contours', diff)

    #find box around contours
    found_contours = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
                                                                                         
        found_contours.append([x, y, w, h])
    #     #check if box is big enough
    #     if w > 70 and h > 70:
    #         cv2.rectangle(diff, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #         #put text with size of box
    #         cv2.putText(diff, str(w) + 'x' + str(h), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
   

    #find biggest box
    biggest_box = [0, 0, 0, 0]
    for box in found_contours:
        if box[2] > biggest_box[2] and box[3] > biggest_box[3]:
            biggest_box = box
    #draw biggest box
    
    if biggest_box[2] > 50 and biggest_box[3] > 50:
        x, y, w, h = biggest_box
        cv2.rectangle(diff, (x, y), (x + w, y + h), (0, 0, 255), 2)
            #put text with size of box
        cv2.putText(diff, str(w) + 'x' + str(h), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('diffrence after box', diff)
    

  












  
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break








diff.show()