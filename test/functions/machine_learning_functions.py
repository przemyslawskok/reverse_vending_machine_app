from functions.syntax import colors as c
# import cv2
# import numpy as np
# from keras.models import load_model
import functions.usb_config as config

def load_cams(machine_class):
    try:
        machine_class.CAMERA_UP = cv2.VideoCapture(config.CAM_UP_INDEX)
        machine_class.CAMERA_LID = cv2.VideoCapture(config.CAM_LID_INDEX)
        print(c.OK_GREEN+"Machine class: Cameras loaded!"+c.ENDC)
        return True
    except:
        print(c.ERROR+ "Machine class: Failed to load cameras!" + c.ENDC)
        return False
def load_models(machine_class):

    print("Machine class: Loading model files...")
    try:
        machine_class.MODEL_UP = load_model('functions/ml_files/model_up.h5')
        machine_class.MODEL_LID = load_model('functions/ml_files/model_lid.h5')
        print(c.OK_GREEN + "Machine class: Model files loaded!" + c.ENDC)
        return True
    except:
        print(c.ERROR + "Machine class: Failed to load model files'! Aborting camera_analysis_worker()" + c.ENDC)
        return False

def photo_model_processing(frame_up,frame_lid):

    image_cutted_up = frame_up[config.CAM_UP_Y_LOW:config.CAM_UP_Y_HIGH, config.CAM_UP_X_LOW:config.CAM_UP_X_HIGH]
    image_cutted_lid = frame_lid[config.CAM_LID_Y_LOW:config.CAM_LID_Y_HIGH,config.CAM_LID_X_LOW:config.CAM_LID_X_HIGH]
 
    frame_up = cv2.resize(image_cutted_up, (224, 224),interpolation=cv2.INTER_AREA)
    frame_lid = cv2.resize(image_cutted_lid, (224, 224),interpolation=cv2.INTER_AREA)

    cv2.imshow('Image up', frame_up)
    cv2.imshow('Image lid', frame_lid)

    frame_up = np.asarray(frame_up, dtype=np.float32).reshape(1, 224, 224, 3)
    frame_lid = np.asarray(frame_lid, dtype=np.float32).reshape(1, 224, 224, 3)

    frame_up = (frame_up / 127.5) - 1
    frame_lid = (frame_lid / 127.5) - 1

    return frame_up, frame_lid


def calculate_model(frame_up,frame_lid,model_up,model_lid):
    

    frame_up, frame_lid = photo_model_processing(frame_up,frame_lid)


    probabilities_up_raw = model_up.predict(frame_up,verbose = 0)
    probabilities_lid_raw = model_lid.predict(frame_lid,verbose = 0)

  
    probabilities_up = []
    probabilities_lid = []


    for probability in probabilities_up_raw[0]:
        probability = round(probability * 100,2)
        probabilities_up.append(probability)

    for probability in probabilities_lid_raw[0]:
        probability = round(probability * 100,2)
        probabilities_lid.append(probability)

    return probabilities_up, probabilities_lid


def check_probabilities_idle(probabilites_up,probabilites_lid):
    if probabilites_up[0] > 80 and probabilites_lid[0] > 80:
        return True
    else:
        return False


def camera_analysis_worker(machine_class):
    print("Machine class: Starting camera analysis worker...")
 
    try:
        camera_up = cv2.VideoCapture(config.CAM_UP_INDEX)
        camera_lid = cv2.VideoCapture(config.CAM_LID_INDEX)
    except:
        print(c.ERROR + "Machine class: Failed to capture cams! Aborting camera_analysis_worker()" + c.ENDC)
        return False
 

    print(c.OK_GREEN+"Machine class: Camera analysis worker started!"+c.ENDC)
    while True:

        r1 , frame_up = camera_up.read()
        r2 , frame_lid = camera_lid.read()
        probabilities_up, probabilities_lid = calculate_model(frame_up,frame_lid,machine_class.MODEL_UP,machine_class.MODEL_LID)
        
        print(probabilities_up,probabilities_lid)

        # if machine_class.STATE_IDLE:
        if not check_probabilities_idle(probabilities_up,probabilities_lid):
            print(c.WARNING+"Machine class: Activity on conveyor belt detected!"+c.ENDC)
            
            machine_class.change_state("STATE_RUNNING")

            
        
    

       
        keyboard_input = cv2.waitKey(1)

