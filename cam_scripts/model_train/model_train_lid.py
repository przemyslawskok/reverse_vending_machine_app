import cv2
import numpy as np
import random

camera = cv2.VideoCapture(0)
record_empty = False
record_plastic = False
record_something = False
record_metal = False
record_glass = False
image_counter = 0
while True:
    image_counter = image_counter + 1
    ret, image = camera.read()
    #cv2.imshow('Before cutting', image)
    #cut the middle of image
    image_cutted = image[40:480,90:530]
    cv2.imshow('After cutting', image_cutted)
    image_cutted = cv2.resize(image_cutted, (224, 224),interpolation=cv2.INTER_AREA)
    cv2.imshow('Resized', image_cutted)
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
    
    if cv2.waitKey(1) & 0xFF == ord('m'):
        print("Starting recording metal")
        record_metal = True

    if cv2.waitKey(1) & 0xFF == ord('g'):
        print("Starting recording glass")
        record_glass = True

    if record_empty:
        cv2.imwrite('images_lid/empty/'+str(image_counter)+'.jpg', image_cutted)
        print('Image saved empty')
        
    if record_plastic:
        cv2.imwrite('images_lid/plastic/'+str(image_counter)+'.jpg', image_cutted)
        print('Image saved plastic')

    if record_something:
        cv2.imwrite('images_lid/something/'+str(image_counter)+'.jpg', image_cutted)
        print('Image saved something')
       
    if record_metal:
        cv2.imwrite('images_lid/metal/'+str(image_counter)+'.jpg', image_cutted)
        print('Image saved metal')

    if record_glass:
        cv2.imwrite('images_lid/glass/'+str(image_counter)+'.jpg', image_cutted)
        print('Image saved glass')


    keyboard_input = cv2.waitKey(1)
    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        record_empty = False
        record_plastic = False
        record_metal = False
        record_something = False
        record_glass = False
        print("Stopped recording")

camera.release()
cv2.destroyAllWindows()
