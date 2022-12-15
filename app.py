import classes
import time

machine=classes.machine()
communication=classes.communication(machine)

while True:
    if machine.STATE_IDLE:
        if len(communication.BARCODES) > 0:
            communication.turn_on_conveyor_belt_backward()
            
            time.sleep(1.2)
            communication.turn_off_conveyor_belt()
        #Check if someone put bottle in hole
        # communication.check_sensor_in_hole()
        # time.sleep(0.1)