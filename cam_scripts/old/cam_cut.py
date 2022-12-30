import cv2
import numpy as np
import random

camera = cv2.VideoCapture(0)
record_empty = False
record_plastic = False
record_something = False
image_counter = 0
while True:
    image_counter = image_counter + 1
    ret, image = camera.read()
    #cv2.imshow('Before cutting', image)


    #cut the middle of image
    image_cutted = image[170:300, 40:580]
    cv2.imshow('After cutting', image_cutted)

    #resize image to 224x224
    image_cutted = cv2.resize(image_cutted, (224, 224), interpolation=cv2.INTER_AREA)
    #cv2.imshow('Resized', image_cutted)
    #if keyboard input is 's' save image to file
    #keyboard input e
    if cv2.waitKey(1) & 0xFF == ord('e'):
    
        print("Starting recording Empty")
        record_empty = True
    if cv2.waitKey(1) & 0xFF == ord('p'):
      
        print("Starting recording Plastic")
        record_plastic = True
    if cv2.waitKey(1) & 0xFF == ord('s'):
    
        print("Starting recording Something")
        record_something = True


    if record_empty:
        
        cv2.imwrite('images/empty/'+str(image_counter)+'.jpg', image_cutted)
        print('Image saved empty')
        
    if record_plastic:
        cv2.imwrite('images/plastic/'+str(image_counter)+'.jpg', image_cutted)

        print('Image saved plastic')


    if record_something:
        
        cv2.imwrite('images/something/'+str(image_counter)+'.jpg', image_cutted)
        print('Image saved something')
       



    keyboard_input = cv2.waitKey(1)
    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        record_empty = False
        record_plastic = False

        record_something = False
        print("Stopped recording")

camera.release()
cv2.destroyAllWindows()
