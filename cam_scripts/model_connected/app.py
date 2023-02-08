import cv2
import numpy as np
from keras.models import load_model

model_up = load_model('model_up.h5')
model_lid = load_model('model_lid.h5')

camera_up = cv2.VideoCapture(0)
camera_lid = cv2.VideoCapture(1)

labels = open('labels.txt', 'r').readlines()


sequence = False
set_of_probabilities = []
probabilities = []



while True:
    ret, image_up = camera_up.read()
    ret2, image_lid = camera_lid.read()

    image_cutted_up = image_up[0:480, 80:560]
    image_cutted_lid = image_lid[40:480,90:530]

    image_up = cv2.resize(image_cutted_up, (224, 224),interpolation=cv2.INTER_AREA)
    image_lid = cv2.resize(image_cutted_lid, (224, 224),interpolation=cv2.INTER_AREA)

    cv2.imshow('Image up', image_up)
    cv2.imshow('Image lid', image_lid)


    image_up = np.asarray(image_up, dtype=np.float32).reshape(1, 224, 224, 3)
    image_lid = np.asarray(image_lid, dtype=np.float32).reshape(1, 224, 224, 3)

    image_up = (image_up / 127.5) - 1
    image_lid = (image_lid / 127.5) - 1

    probabilities_up_raw = model_up.predict(image_up,verbose = 0)
    probabilities_lid_raw = model_lid.predict(image_lid,verbose = 0)

  
    probabilities_up = []
    probabilities_lid = []


    for probability in probabilities_up_raw[0]:
        probability = round(probability * 100,2)
        probabilities_up.append(probability)

    for probability in probabilities_lid_raw[0]:
        probability = round(probability * 100,2)
        probabilities_lid.append(probability)

    if probabilities_up[4] < 50 and probabilities_lid[4] < 50:
        if not sequence:
            print("Starting sequence")
            sequence = True
            set_of_probabilities = []

    if sequence:
        avarage_probabilities = []
  
        
        print("UP: ", str(probabilities_up) , "LID: ", str(probabilities_lid))

        avarage_probabilities.append(round((probabilities_up[0]+probabilities_lid[0])/2 , 2))
        avarage_probabilities.append(round((probabilities_up[1]+probabilities_lid[1])/2 , 2))
        avarage_probabilities.append(round((probabilities_up[2]+probabilities_lid[2])/2 , 2))
        avarage_probabilities.append(round((probabilities_up[3]+probabilities_lid[3])/2 , 2))
        avarage_probabilities.append(round((probabilities_up[4]+probabilities_lid[4])/2 , 2))

        set_of_probabilities.append(avarage_probabilities)
      

        if probabilities_up[4] > 60 or probabilities_lid[4] > 60:
            print("Sequence ended")
            sequence = False

            #calculate avarage values of sets
            
            first_value = None
            second_value = None
            third_value = None
            fourth_value = None
            fifth_value = None


            for set in set_of_probabilities:
                
                if first_value:
                    first_value += set[0]
                else:
                    first_value = set[0]

                if second_value:
                    second_value += set[1]
                else:
                    second_value = set[1]

                if third_value:
                    third_value += set[2]
                else:
                    third_value = set[2]
                
                if fourth_value:
                    fourth_value += set[3]
                else:
                    fourth_value = set[3]
                
                if fifth_value:
                    fifth_value += set[4]
                else:
                    fifth_value = set[4]

                
            first_value = round(first_value / len(set_of_probabilities),2)
            second_value = round(second_value / len(set_of_probabilities),2)
            third_value = round(third_value / len(set_of_probabilities),2)
            fourth_value = round(fourth_value / len(set_of_probabilities),2)
            fifth_value = round(fifth_value / len(set_of_probabilities),2)


            print("First value: ", first_value)
            print("Second value: ", second_value)
            print("Third value: ", third_value)
            print("Fourth value: ", fourth_value)
            print("Fifth value: ", fifth_value)

                


    keyboard_input = cv2.waitKey(1)
    if keyboard_input == 27:
        break
