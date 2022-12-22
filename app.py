import classes
import time
import syntax as s
import database_functions as db
import machine_functions as mf
machine=classes.machine()
communication=classes.communication(machine)
synchronization=classes.synchronization(machine,communication)
while True:
    if machine.STATE_IDLE:
        if len(communication.BARCODES) > 0:
            bottle_info = db.get_bottle_information(communication.BARCODES[0])
            if bottle_info:
                #check material
                if bottle_info[3] == "Plastic":
                    print(s.colors.OK_CYAN+"Main loop: Bottle material is Plastic, taking bottle"+s.colors.ENDC)
                    communication.turn_on_red_led()
                    communication.turn_on_conveyor_belt_forward()
                    while machine.RING_SENSOR:
                        continue
                    #ask about weight
                    time.sleep(0.2)
                    communication.get_weight()
                    time.sleep(0.2)
                    if mf.compare_bottle_weight(bottle_info,communication):
                        print(s.colors.OK_CYAN+"Main loop: Bottle weight is OK, taking bottle"+s.colors.ENDC)
                        #wait for bottle to be taken
                        while not machine.BOTTLE_END_SENSOR:
                            continue
                        time.sleep(0.7)
                        communication.turn_on_green_led()
                        communication.turn_off_conveyor_belt()
                        communication.BARCODES = []
                    else:
                        communication.turn_on_conveyor_belt_backward()
                        while not machine.RING_SENSOR:
                            continue
                        time.sleep(0.1)
                        communication.turn_on_red_led()
                        communication.turn_off_conveyor_belt()
                        communication.BARCODES = []
                      

       











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


