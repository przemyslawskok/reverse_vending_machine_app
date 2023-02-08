import classes
import time
import functions.syntax as s
import functions.usb_config as config
import functions.database_functions as db
import functions.machine_functions as mf

from keras.models import load_model
import cv2



machine=classes.machine()

communication=classes.communication(machine)

synchronization=classes.synchronization(machine,communication)



communication.turn_off_cam_led()
communication.turn_off_conveyor_belt()
communication.turn_on_green_led()


i = 0
while True:
    
    if not machine.SEQUENCE:
        i +=1
        if i == 5000000:
            i = 0

            communication.get_weight()
            communication.TARE_STATUS = False
    else:
        if machine.STATES["STATE_READY"]:
            if len(communication.BARCODES) > 0:
                print(s.colors.OK_CYAN+"Main loop: Barcode detected"+s.colors.ENDC)
                communication.LAST_BARCODE = communication.BARCODES[0]
                if db.get_bottle_information(communication.LAST_BARCODE,machine):
                    machine.change_state("STATE_RUNNING",communication)
                else:
                    print(s.colors.ERROR+"Main loop: Barcode not in database"+s.colors.ENDC)
                    communication.BARCODES=[]
            # elif machine.BOTTLE_IN_RING:
            #     print(s.colors.OK_CYAN+"Main loop: Object detected in ring"+s.colors.ENDC)

        
        elif machine.STATES["STATE_RUNNING"]:
            if not machine.BOTTLE_IN_RING:
                if machine.RING_SENSOR:
                    print(s.colors.OK_CYAN+"Main loop: Ring sensor detected object"+s.colors.ENDC)
                    machine.BOTTLE_IN_RING = True
            elif machine.BOTTLE_IN_RING:
                if not machine.BOTTLE_ON_CONVEYOR_BELT:
                    print(s.colors.OK_CYAN+"Main loop: Bottle in ring, waiting for bottle on conveyor belt"+s.colors.ENDC)
                    if not machine.RING_SENSOR:
                        print(s.colors.OK_CYAN+"Main loop: Ring sensor empty"+s.colors.ENDC)
                        machine.BOTTLE_IN_RING = False
                        machine.BOTTLE_ON_CONVEYOR_BELT = True
                        print(s.colors.OK_CYAN+"Main loop: Bottle on conveyor belt"+s.colors.ENDC)
                        # communication.turn_on_conveyor_belt_forward()
                        # communication.turn_on_cam_led()
            if machine.BOTTLE_ON_CONVEYOR_BELT:
                if not machine.ASKED_ABOUT_WEIGHT:
                    time.sleep(0.5)
                    communication.get_weight()
                    machine.ASKED_ABOUT_WEIGHT = True
                    machine.WEIGHED_BOTTLE = False
                if machine.BOTTLE_END_SENSOR:
                    print(s.colors.OK_CYAN+"Main loop: Bottle end sensor detected"+s.colors.ENDC)

                if machine.WEIGHED_BOTTLE:
                    if mf.compare_bottle_size(communication.WEIGHT_VALUE,machine.DB_WEIGHT,machine):
                        print(s.colors.OK_GREEN+"Main loop: Bottle weight OK"+s.colors.ENDC)
                        machine.BOTTLE_ON_CONVEYOR_BELT = False
                        machine.ASKED_ABOUT_WEIGHT = False
                        mf.add_bottle_to_sequence(communication,communication.LAST_BARCODE)

                        machine.change_state("STATE_RUNNING_CRUSHING",communication)
                    
                    else:
                        machine.BOTTLE_ON_CONVEYOR_BELT = False
                        machine.ASKED_ABOUT_WEIGHT = False
                        communication.turn_on_conveyor_belt_backward()
                        machine.change_state("STATE_RUNNING_GIVING",communication)
                
        elif machine.STATES["STATE_RUNNING_GIVING"]:
            print(s.colors.OK_CYAN+"Main loop: Giving bottle"+s.colors.ENDC)
            if not machine.RING_SENSOR:
                print(s.colors.OK_CYAN+"Main loop: Ring sensor empty, waiting for bottle to come to ring"+s.colors.ENDC)
            else:
                print(s.colors.OK_CYAN+"Main loop: Bottle in ring, waiting for bottle to be taken"+s.colors.ENDC)
                machine.change_state("STATE_WAITING_FOR_TAKE",communication)

        elif machine.STATES["STATE_RUNNING_CRUSHING"]:
            print(s.colors.OK_CYAN+"Main loop: Trying to crush bottle"+s.colors.ENDC)
            if not machine.BOTTLE_END_SENSOR:
                print(s.colors.OK_CYAN+"Main loop: Bottle end sensor empty, waiting for bottle to be crushed"+s.colors.ENDC)
            else:
                print(s.colors.OK_CYAN+"Main loop: Bottle crushed"+s.colors.ENDC)
                machine.change_state("STATE_READY",communication)           
                communication.BARCODES=[]
        
        elif machine.STATES["STATE_WAITING_FOR_TAKE"]:
            print(s.colors.OK_CYAN+"Main loop: Waiting for bottle to be taken"+s.colors.ENDC)
            time.sleep(0.5)
            if not machine.RING_SENSOR:
                print(s.colors.OK_CYAN+"Main loop: Ring sensor empty, bottle taken"+s.colors.ENDC)
                machine.change_state("STATE_READY",communication)
                time.sleep(5)
                communication.BARCODES=[]

        elif machine.STATES["STATE_SUCCESS"]:
            mf.print_receipt(communication)
            machine.change_state("STATE_IDLE",communication)

        # communication.get_weight()
            # communication.TARE_STATUS = True
            #check if there is any barcode
            











    # if machine.UNKOWN_OBJECT:
    #     print(s.colors.ERROR+"Main loop: Unknown object detected, stopping conveyor belt"+s.colors.ENDC)
    #     print("U. O.:",machine.UNKOWN_OBJECT, " MATERIAL:",machine.BOTTLE_MATERIAL," SIZE:", machine.BOTTLE_SIZE," WEIGHT:",communication.WEIGHT_VALUE)
    #     machine.UNKOWN_OBJECT = False
    #     communication.turn_on_conveyor_belt_backward()
    #     time.sleep(3)
    #     communication.turn_on_conveyor_belt_forward()
    # else:
    #     if machine.CHECK_BOTTLE:
    #         print(s.colors.OK_CYAN+"Main loop: Checking bottle"+s.colors.ENDC)
    #         try:
    #             machine.DB_NAME, machine.DB_MATERIAL, machine.DB_WEIGHT, machine.DB_SIZE, machine.DB_LENGTH = db.get_bottle_information(communication.BARCODES[0])
    #         except:
    #             machine.DB_NAME = "unkown"
    #             machine.DB_MATERIAL = "unkown"
    #             machine.DB_WEIGHT = 0
    #             machine.DB_SIZE = 0
    #             machine.DB_LENGTH = 0

    #         machine.CHECK_BOTTLE = False
    #         communication.get_weight()
    #         time.sleep(0.15)
    #         print("U. O.:",machine.UNKOWN_OBJECT, " MATERIAL:",machine.BOTTLE_MATERIAL," SIZE:", machine.BOTTLE_SIZE," WEIGHT:",communication.WEIGHT_VALUE)
    #         communication.turn_on_conveyor_belt_backward()
    #         time.sleep(3)
    #         communication.turn_on_conveyor_belt_forward()
    # continue
    # if machine.STATE_IDLE:
    #     # if len(communication.BARCODES) > 0:
    #     r1 , frame_up = CAMERA_UP.read()
    #     r2 , frame_lid = CAMERA_LID.read()


    #     cv2.imshow('Image up', frame_up)
    #     cv2.imshow('Image lid', frame_lid)


    #     probabilities_up, probabilities_lid = ml.calculate_model(frame_up,frame_lid,MODEL_UP,MODEL_LID)
        
    #     print(probabilities_up,probabilities_lid)


    #     keyboard_input = cv2.waitKey(1)








    #     # if len(communication.BARCODES) > 0:
    #     #     bottle_info = db.get_bottle_information(communication.BARCODES[0])
    #     #     if bottle_info:
        #         #check material
        #         if bottle_info[3] == "Plastic":
        #             print(s.colors.OK_CYAN+"Main loop: Bottle material is Plastic, taking bottle"+s.colors.ENDC)
        #             communication.turn_on_red_led()
        #             communication.turn_on_conveyor_belt_forward()
        #             while machine.RING_SENSOR:
        #                 continue
        #             #ask about weight
        #             time.sleep(0.2)
        #             communication.get_weight()
        #             time.sleep(0.2)
        #             if mf.compare_bottle_weight(bottle_info,communication):
        #                 print(s.colors.OK_CYAN+"Main loop: Bottle weight is OK, taking bottle"+s.colors.ENDC)
        #                 #wait for bottle to be taken
        #                 while not machine.BOTTLE_END_SENSOR:
        #                     continue
        #                 time.sleep(0.7)
        #                 communication.turn_on_green_led()
        #                 communication.turn_off_conveyor_belt()
        #                 communication.BARCODES = []
        #             else:
        #                 communication.turn_on_conveyor_belt_backward()
        #                 while not machine.RING_SENSOR:
        #                     continue
        #                 time.sleep(0.1)
        #                 communication.turn_on_red_led()
        #                 communication.turn_off_conveyor_belt()
        #                 communication.BARCODES = []
                      

       











    # communication.turn_on_conveyor_belt_forward()
    # time.sleep(1)
    # communication.turn_on_conveyor_belt_backward()
    # time.sleep(1)
    # communication.turn_off_conveyor_belt()
    # time.sleep(1)
    # communication.turn_on_green_led()
    # time.sleep(1)
    # communication.turn_on_red_led()
    # time.sleep(1)
    # if machine.STATE_IDLE:
    #     if len(communication.BARCODES) > 0 or machine.RING_SENSOR:

    #         machine.STATE_IDLE = False
    #         machine.STATE_ACTIVE_READY = True
    #         communication.turn_on_conveyor_belt_forward()
    #         # communication.turn_on_conveyor_belt_forward()
    #         # time.sleep(1)
    #         # #spytaj o wage
            
    #         # communication.get_weight()
    #         # time.sleep(0.2)
    #         # if communication.WEIGHT_VALUE > 1000000:
    #         #     print(s.colors.OK_CYAN+"Main loop: Weight value is too high, giving out bottle"+s.colors.ENDC)
    #         #     communication.turn_on_conveyor_belt_backward()
    #         #     time.sleep(1.5)
    #         # else:
    #         #     print(s.colors.OK_CYAN+"Main loop: Weight value is OK, taking bottle"+s.colors.ENDC)
    #         #     communication.turn_on_conveyor_belt_forward()
    #         #     time.sleep(1.5)

    #         # print(s.colors.OK_CYAN+"Main loop: Turning off conveyor belt"+s.colors.ENDC)
    #         # communication.turn_off_conveyor_belt()
    #         # communication.BARCODES = []
    #         # time.sleep(3)
    # elif  machine.STATE_ACTIVE_READY:
    #     if not machine.RING_SENSOR:
    #         time.sleep(0.1)
    #         if not machine.RING_SENSOR:
    #             communication.get_weight()
    #             time.sleep(0.2)
    #             if communication.WEIGHT_VALUE > 1000000:
    #                 print(s.colors.OK_CYAN+"Main loop: Weight value is too high, giving out bottle"+s.colors.ENDC)
    #                 communication.turn_on_conveyor_belt_backward()
    #                 time.sleep(1.5)
    #             else:
    #                 print(s.colors.OK_CYAN+"Main loop: Weight value is OK, taking bottle"+s.colors.ENDC)
    #                 machine.STATE_ACTIVE_RUNNING = True
    #                 machine.STATE_ACTIVE_READY = False
    # elif machine.STATE_ACTIVE_RUNNING:
    #     if machine.BOTTLE_END_SENSOR:
    #         communication.turn_off_conveyor_belt()
    #         machine.STATE_ACTIVE_RUNNING = False
    #         machine.STATE_ACTIVE_READY = False
    #         machine.STATE_IDLE = True
    #         communication.WEIGHT_VALUE = 0
    #         communication.BARCODES = []


