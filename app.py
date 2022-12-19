import classes
import time
import syntax as s
machine=classes.machine()
communication=classes.communication(machine)

while True:
    if machine.STATE_IDLE:
        if len(communication.BARCODES) > 0 or machine.RING_SENSOR:
            communication.turn_on_conveyor_belt_backward()
            time.sleep(1)
            #spytaj o wage
            
            communication.get_weight()
            time.sleep(0.05)
            if communication.WEIGHT_VALUE > 1000000:
                print(s.colors.OK_CYAN+"Main loop: Weight value is too high, giving out bottle"+s.colors.ENDC)
                communication.turn_on_conveyor_belt_forward()
                time.sleep(1.5)
            else:
                print(s.colors.OK_CYAN+"Main loop: Weight value is OK, taking bottle"+s.colors.ENDC)
                communication.turn_on_conveyor_belt_backward()
                time.sleep(1.5)

            print(s.colors.OK_CYAN+"Main loop: Turning off conveyor belt"+s.colors.ENDC)
            communication.turn_off_conveyor_belt()
            communication.BARCODES = []
            time.sleep(3)
        