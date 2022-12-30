import _thread
import usb_config
import communication_functions as cf
import synchronization_functions as sf
import time
from syntax import colors as c


class machine():

    def __init__(self):
        print("Machine class: Initializing...")
        
        
        #machine states
        self.STATE_IDLE = True              #Machine right there is waiting for user to start the process by putting bottle in hole
        self.STATE_ACTIVE_READY = False     #Machine is waiting for user to scan barcode of bottle or put out bottle from hole          
        self.STATE_ACTIVE_RUNNING = False   #Machine is waiting for user to get out hand of and start the bottle crushing process
    
        self.STATE_SAFE_MODE = False        #Critical state

        self.STARTING_SEQUENCE = False      
        self.CONVEYOUR_BELT = False         #F - Forward, B - Backward, False - Stop
        self.RING_SENSOR = False            #True - Object in ring detected, False - Ring empty
        self.BOTTLE_END_SENSOR = False      #True - Object on end on conveyor belt detected, False - Empty 
        self.VALVE_SENSOR = False           #True - Object near valve, False - No object near valve
        self.PRINTER_SPOOL = 0              #Integer - Number of % of spool left
        self.BIN_FILLING_LEVEL = 0          #Integer - Number of % of bin filling level
        

        print(c.OK_GREEN+"Machine class: Initialized!"+c.ENDC)


       


class communication():
    def __init__(self,machine_class):
        print("Communication class: Initializing...")


        self.machine = machine_class
 
        self.STM32_STATUS = False           #True - Connected, False - Disconnected
        self.PRINTER_STATUS = False         #True - Connected, False - Disconnected
        self.SCANNERS_STATUS = False        #True - Connected, False - Disconnected

        self.BARCODES = []                  #List of scanned barcodes
        self.BARCODES_TIMER = -1            #Timer for clearing barcodes list

        self.WEIGHT_VALUE = 0               #Integer - Weight value 


        
        self.TURN_ON_CONVEYOR_BELT_FORWARD = False
        self.TURN_ON_CONVEYOR_BELT_BACKWARD = False
        self.TURN_OFF_CONVEYOR_BELT = False
        self.TURN_ON_RED_LED = False
        self.TURN_ON_GREEN_LED = False
        self.TURN_ON_BLINKING_RED_LED = False
        self.TURN_ON_CAM_LED = False
        self.TURN_OFF_CAM_LED = False


        self.GET_WEIGHT = False
        
        

        _thread.start_new_thread(cf.check_connected_devices_worker,(self,))
       
        # while not (self.STM32_STATUS and self.PRINTER_STATUS and self.SCANNERS_STATUS):
            # print(c.WARNING+"Communication class: Waiting for devices to connect..."+c.ENDC)
            # time.sleep(1)
        print("Communication class: All devices connected, starting reading and writing threads...")



        _thread.start_new_thread(cf.STM32_communication_buffor,(self,))
        _thread.start_new_thread(cf.scanners_communication_buffor,(self,))
        _thread.start_new_thread(cf.barcodes_timer_worker,(self,))



        print(c.OK_GREEN+"Communication class: Initialized!"+c.ENDC)
    
    def turn_on_conveyor_belt_forward(self):
        self.TURN_ON_CONVEYOR_BELT_FORWARD = True
    def turn_on_conveyor_belt_backward(self):
        self.TURN_ON_CONVEYOR_BELT_BACKWARD = True
    def turn_off_conveyor_belt(self):
        self.TURN_OFF_CONVEYOR_BELT = True
    def turn_on_green_led(self):
        self.TURN_ON_GREEN_LED = True
    def turn_on_red_led(self):
        self.TURN_ON_RED_LED = True
    def turn_blinking_red_led(self):
        self.TURN_ON_BLINKING_RED_LED = True
    def get_weight(self):
        self.GET_WEIGHT = True



class synchronization():
    def __init__(self,machine_class,communication_class):
        
        print("Synchronization class: Initializing...")
        self.machine = machine_class
        self.communication = communication_class

        if not sf.validate_bottles_table():
            self.machine.STATE_SAFE_MODE = True


        #_thread.start_new_thread(sf.synchronization_worker,(self,))
        #_thread.start_new_thread(sf.update_information_worker,(self,))

        print(c.OK_GREEN+"Synchronization class: Initialized!"+c.ENDC)