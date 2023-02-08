import cv2
import numpy as np
import socket
import _thread
import time
from PIL import Image, ImageChops

import functions.usb_config as config
import functions.machine_learning_functions as ml
from functions.syntax import colors as c

class information():
    can_start = True

info = information()


CAMERA_UP, CAMERA_LID = ml.load_cams()
MODEL_UP, MODEL_LID = ml.load_models()

sequence = False
set_of_probabilities = []

#sizing
background = Image.open('ml_files/background.jpg')
#background = None



def send_message(probabilites_up,probabilies_lid, bottle_length):
    if probabilies_lid and probabilites_up:
        avarage = []
        for i in range(len(probabilites_up)):
            avarage.append(round((probabilites_up[i] + probabilies_lid[i])/2, 2))
        
        string = ""
        for i in range(len(avarage)):
            string += str(avarage[i]) + "_"
        string = string[:-1]
        message = "ml@" + string
    else:
        message = "ml@false"
        
    if bottle_length:
        message += "@" + str(bottle_length)
    else:
        message += "@false"
    try:
        s = socket.socket()        
        s.connect((config.BACKEND_HOST, config.BACKEND_PORT))
        # print("Sending message: ",message)
        s.send(message.encode())
    except:
        print(c.ERROR + "Failed to send data to backend!" + c.ENDC)

def avarage_probabilities(set_of_probabilities,probabilities_up,probabilities_lid):
    avarage_probabilities = []

    avarage_probabilities.append(round((probabilities_up[0]+probabilities_lid[0])/2 , 2))
    avarage_probabilities.append(round((probabilities_up[1]+probabilities_lid[1])/2 , 2))
    avarage_probabilities.append(round((probabilities_up[2]+probabilities_lid[2])/2 , 2))
    avarage_probabilities.append(round((probabilities_up[3]+probabilities_lid[3])/2 , 2))
    avarage_probabilities.append(round((probabilities_up[4]+probabilities_lid[4])/2 , 2))
    set_of_probabilities.append(avarage_probabilities)
    return set_of_probabilities

def measure_bottle(background):

    live_image = Image.open('ml_files/live.jpg')
    diffrence = ImageChops.difference(background, live_image)
    diffrence.save('ml_files/diffrence.jpg')
    diffrence = cv2.imread('ml_files/diffrence.jpg')
    #cv2.imshow('diffrencerence before gray', diffrence)
    diffrence_gray = cv2.cvtColor(diffrence, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('diffrencerence after gray', diffrence_gray)
    #treshhold
    ret, diffrence_gray = cv2.threshold(diffrence_gray, 40, 255, cv2.THRESH_BINARY)
    #cv2.imshow('diffrencerence after treshhold', diffrence_gray)

    #find contours
    contours, hierarchy = cv2.findContours(diffrence_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(diffrence, contours, -1, (0, 0, 255), 3)
    cv2.imshow('diffrencerence after contours', diffrence)

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
            
    
    middle_point = biggest_box[0]+(biggest_box[2]/2)
    middle_point = int(middle_point)
    print("middlepoint at X:", middle_point)
    start_x = biggest_box[0]
    end_x = biggest_box[0]+biggest_box[2]
    print("START X: ", biggest_box[0])
    print("END X: ", biggest_box[0]+biggest_box[2])
    if (start_x>10) or (start_x == 0 and end_x > 200):
        print("Bottle on conveyor")
        size_of_bottle = [biggest_box[2],biggest_box[3],biggest_box[2]*biggest_box[3]]
        #divide all elements of list by variable config.scale
        size_of_bottle = [round(x / config.PX_FACTOR, 2) for x in size_of_bottle]

        cv2.circle(image_back, (biggest_box[0], biggest_box[1]), 5, (255, 0, 0), -1)
        cv2.circle(image_back , (biggest_box[0] +biggest_box[2] , biggest_box[1]), 5, (255, 255, 0), -1)
        cv2.imshow('CIRCLE', image_back)

        send_message(False, False, size_of_bottle[0])
        return size_of_bottle
    # if middle_point > 98 and middle_point < 120:
    #     print("middle found")
    #     size_of_bottle = [biggest_box[2],biggest_box[3],biggest_box[2]*biggest_box[3]]
    #     cv2.circle(image_back, (biggest_box[0], biggest_box[1]), 5, (255, 0, 0), -1)
    #     cv2.circle(image_back, (biggest_box[0] +biggest_box[2] , biggest_box[1]), 5, (255, 255, 0), -1)
    #     cv2.imshow('CIRCLE', image_back)
    #     return size_of_bottle
    else:
        return False



while True:
    r1 , frame_up = CAMERA_UP.read()
    r2 , frame_lid = CAMERA_LID.read()
    
 
    #measuring size of bottle
    size_photo = frame_up[0:448, 80:528]
    image_back = cv2.resize(size_photo, (0,0), fx=0.5, fy=0.5)
    cv2.imwrite('ml_files\live.jpg', image_back)
    
    probabilities_up, probabilities_lid = ml.calculate_model(frame_up,frame_lid,MODEL_UP,MODEL_LID)
    #check size of bottle
    print(probabilities_up,probabilities_lid)
    send_message(probabilities_up,probabilities_lid, bottle_length=False)
   
    if probabilities_up[4] > 50 and probabilities_lid[4] > 50:
        cv2.imwrite('ml_files/background.jpg', image_back)
        try:
            background = Image.open('ml_files/background.jpg')
        except:
            print("Failed to load background")
    else: 
        measure_bottle(background)

    keyboard_input = cv2.waitKey(1)