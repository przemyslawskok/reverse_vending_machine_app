import cv2
import numpy as np
from keras.models import load_model
from PIL import Image, ImageChops

# Load the model
model = load_model('keras_model.h5')

# CAMERA can be 0 or 1 based on default camera of your computer.
camera = cv2.VideoCapture(0)

# Grab the labels from the labels.txt file. This will be used later.
labels = open('labels.txt', 'r').readlines()



started_sequence = False
sequence_counter = 0
sequence = []
size_of_bottle = []



background = Image.open('static.jpg')

while True:
    # Grab the webcameras image.
    ret, image = camera.read()
    # Resize the raw image into (224-height,224-width) pixels.
    image_cutted = image[0:448, 80:528]


    #resize image 2x smaller
    image = cv2.resize(image_cutted, (0,0), fx=0.5, fy=0.5)
    image_back = cv2.resize(image_cutted, (0,0), fx=0.5, fy=0.5)
    cv2.imwrite('live.jpg', image_back)
    # Show the image in a window
    cv2.imshow('Webcam Image', image)
    
    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    # Normalize the image array
    image = (image / 127.5) - 1
    # Have the model predict what the current image is. Model.predict
    # returns an array of percentages. Example:[0.2,0.8] meaning its 20% sure
    # it is the first label and 80% sure its the second label.
    probabilities = model.predict(image)
    # Print what the highest value probabilitie label
    
    results = []
    for result in probabilities[0]:
        results.append(int(float(result)*100))
        


    if results[0] < 90 and not started_sequence:
        print("Starting sequence")
        started_sequence = True

    if results[0] > 90 and started_sequence:
        print("Stopping sequence")
        started_sequence = False
       


    if started_sequence:
        #count the avarage of every result
        sequence_counter = sequence_counter + 1
        if sequence == []:
            sequence = results
        else:
            for index, result in enumerate(results):
                sequence[index] = sequence[index] + result




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

        #find biggest box
        biggest_box = [0, 0, 0, 0]
        for box in found_contours:
            if box[2] > biggest_box[2] and box[3] > biggest_box[3]:
                biggest_box = box
                #draw X and Y point 
                

        #draw box
        cv2.rectangle(image_back, (biggest_box[0], biggest_box[1]), (biggest_box[0] + biggest_box[2], biggest_box[1] + biggest_box[3]), (0, 255, 0), 2)
    
        
        middle_point = biggest_box[0]+(biggest_box[2]/2)
        middle_point = int(middle_point)
        if middle_point > 98 and middle_point < 120:
            print("middle")
            size_of_bottle = [biggest_box[2],biggest_box[3],biggest_box[2]*biggest_box[3]]
            cv2.circle(image_back, (biggest_box[0], biggest_box[1]), 5, (255, 0, 0), -1)
            cv2.circle(image_back, (biggest_box[0] +biggest_box[2] , biggest_box[1]), 5, (255, 255, 0), -1)
            cv2.imshow('CIRCLE', image_back)
            







    if not started_sequence:
        if not sequence == []:
            sequence = [x / sequence_counter for x in sequence]
            print(sequence)
            print(size_of_bottle)
            sequence = []
            sequence_counter = 0
            size_of_bottle = []
            



    
    #convert values from probabilities to percentage
 


    if sequence == []:
        cv2.imwrite('static.jpg', image_back)
        background = Image.open('static.jpg')
        









    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)
    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()
