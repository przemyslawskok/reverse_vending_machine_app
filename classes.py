import _thread
import functions.usb_config as usb_config
import functions.communication_functions as cf
import functions.synchronization_functions as sf
import time
from functions.syntax import colors as c


class machine():

    def __init__(self):
        print("Machine class: Initializing...")
        
        
        #machine states
        self.STATE_IDLE = True              #Machine right there is waiting for user to start the process by putting bottle in hole
        self.STATE_READY = False
        self.STATE_RUNNING = False
        self.STATE_RUNNING_GIVING = False
        self.STATE_WAITING_FOR_TAKE = False
        self.STATE_RUNNING_CRUSHING = False
        self.STATE_SUCCESS = False

        self.STATE_SAFE_MODE = False        #Critical state


        self.STATES = {
            "STATE_IDLE":self.STATE_IDLE,
            "STATE_READY":self.STATE_READY,
            "STATE_RUNNING":self.STATE_RUNNING,
            "STATE_RUNNING_GIVING":self.STATE_RUNNING_GIVING,
            "STATE_WAITING_FOR_TAKE":self.STATE_WAITING_FOR_TAKE,
            "STATE_RUNNING_CRUSHING":self.STATE_RUNNING_CRUSHING,
            "STATE_SUCCESS":self.STATE_SUCCESS,
            "STATE_SAFE_MODE":self.STATE_SAFE_MODE
        }


        self.STARTING_SEQUENCE = False      
        self.CONVEYOUR_BELT = False         #F - Forward, B - Backward, False - Stop
        self.RING_SENSOR = False            #True - Object in ring detected, False - Ring empty
        self.BOTTLE_END_SENSOR = False      #True - Object on end on conveyor belt detected, False - Empty 
        self.PRINTER_SPOOL = 0              #Integer - Number of % of spool left
        self.BIN_FILLING_LEVEL = 0          #Integer - Number of % of bin filling level
        

        self.BOTTLE_ON_CONVEYOR_BELT = False     #True - Bottle on conveyor belt, False - No bottle on conveyor belt 
        self.BOTTLE_IN_RING = False              #True - Bottle in ring, False - No bottle in ring
        self.ASKED_ABOUT_WEIGHT = False              #True - Bottle was weighed, False - Bottle was not weighed
        self.WEIGHED_BOTTLE = False              #True - Bottle was weighed, False - Bottle was not weighed

        self.BOTTLE_MATERIAL = ""           #String - Material of bottle
        self.BOTTLE_WEIGHT = 0              #Integer - Weight of bottle
        self.BOTTLE_SIZE = ""                #String - Size of bottle
        self.BOTTLE_LENGTH = 0
        self.BOTTLE_PROBABILITIES = [None,None,None,None,None]      #List - Probabilities of bottle material
        self.CHECK_BOTTLE = False

        self.SEQUENCE = False

        self.SEQUENCE_ARRAY = []


        self.DB_SIZE = ""
        self.DB_MATERIAL = ""
        self.DB_WEIGHT = 0
        self.DB_LENGTH = 0
        self.DB_NAME = ""


        self.WEIGHT_DB_DIFFRENCE = 0


        self.UNKOWN_OBJECT = False          #True - Unknown object detected, False - No unknown object detected
        self.ANALYZE_UNKOWN_OBJECT = False
        self.SET_OF_PROBABILITIES = []
        print(c.OK_GREEN+"Machine class: Initialized!"+c.ENDC)



    def change_state(self,state,communication_class):
        #change every state to false
        for key in self.STATES:
            if key != state:
                self.STATES[key] = False
            else:
                print(c.OK_BLUE+"Machine class: Changing state to: "+c.OK_GREEN+state+c.ENDC)
                self.STATES[key] = True




        if state == "STATE_IDLE":
            communication_class.turn_on_red_led()
            communication_class.turn_off_cam_led()
            communication_class.turn_off_conveyor_belt()

            communication_class.TARE_STATUS = False
            communication_class.machine.SEQUENCE = False
            communication_class.machine.SEQUENCE_ARRAY = []


        elif state == "STATE_READY":
            communication_class.turn_on_green_led()
            communication_class.turn_on_cam_led()
            communication_class.turn_off_conveyor_belt()

            communication_class.TARE_STATUS = True
            communication_class.machine.SEQUENCE = True
            communication_class.machine.UNKOWN_OBJECT = False

        elif state == "STATE_RUNNING":
            communication_class.turn_on_conveyor_belt_forward()
            communication_class.turn_on_red_led()
        elif state == "STATE_RUNNING_GIVING":
            communication_class.turn_on_blinking_red_led()
        elif state == "STATE_WAITING_FOR_TAKE":
            communication_class.turn_on_blinking_red_led()
            communication_class.turn_off_conveyor_belt()
        elif state == "STATE_RUNNING_CRUSHING":
            communication_class.turn_on_red_led()
        elif state == "STATE_SUCCESS":
            communication_class.turn_on_red_led()
        elif state == "STATE_SAFE_MODE":
            print(c.ERROR + "Machine class: Turning safe mode!" + c.ENDC)
      

        # if state == "STATE_IDLE":
        #     self.STATE_IDLE = True           
        #     communication_class.turn_on_green_led()
        #     communication_class.turn_off_cam_led()
        #     communication_class.turn_off_conveyor_belt()


        #     self.STATE_RUNNING = False
        #     self.STATE_RUNNING_GIVING = False
        #     self.STATE_SAFE_MODE = False 
        #     self.STATE_WAITING_FOR_TAKE = False
        #     self.STATE_RUNNING_CRUSHING = False

        # elif state == "STATE_RUNNING":
        #     self.STATE_RUNNING = True           
        #     communication_class.turn_on_red_led()

        #     self.STATE_IDLE = False
        #     self.STATE_RUNNING_GIVING = False
        #     self.STATE_SAFE_MODE = False 
        #     self.STATE_WAITING_FOR_TAKE = False
        #     self.STATE_RUNNING_CRUSHING = False

        # elif state == "STATE_RUNNING_GIVING":
        #     self.STATE_RUNNING_GIVING = True           
        #     communication_class.turn_on_blinking_red_led()

        #     self.STATE_IDLE = False
        #     self.STATE_RUNNING = False
        #     self.STATE_SAFE_MODE = False
        #     self.STATE_WAITING_FOR_TAKE = False
        #     self.STATE_RUNNING_CRUSHING = False

        # elif state == "STATE_WAITING_FOR_TAKE":
        #     self.STATE_WAITING_FOR_TAKE = True           
        #     communication_class.turn_on_blinking_red_led()
        #     communication_class.turn_off_conveyor_belt()

        #     self.STATE_IDLE = False
        #     self.STATE_RUNNING = False
        #     self.STATE_RUNNING_GIVING = False
        #     self.STATE_SAFE_MODE = False
        #     self.STATE_RUNNING_CRUSHING = False

        # elif state == "STATE_RUNNING_CRUSHING":
        #     self.STATE_RUNNING_CRUSHING = True           
        #     communication_class.turn_on_red_led()

        #     self.STATE_IDLE = False
        #     self.STATE_RUNNING = False
        #     self.STATE_RUNNING_GIVING = False
        #     self.STATE_SAFE_MODE = False
        #     self.STATE_WAITING_FOR_TAKE = False






        # elif state == "STATE_SAFE_MODE":
        #     print(c.ERROR + "Machine class: Turning safe mode!" + c.ENDC)
        #     self.STATE_SAFE_MODE = True           

        #     self.STATE_IDLE = False
        #     self.STATE_RUNNING = False
        #     self.STATE_RUNNING_GIVING = False
        #     self.STATE_WAITING_FOR_TAKE = False
        #     self.STATE_RUNNING_CRUSHING = False

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
        self.LAST_BARCODE = "000000000000"

        self.ML_BUFFOR = []                 #Buffor for keeping last message
        self.ML_BUFFOR_UPDATE = False       #True - Update buffor, False - No update


        self.TURN_ON_CONVEYOR_BELT_FORWARD = False
        self.TURN_ON_CONVEYOR_BELT_BACKWARD = False
        self.TURN_OFF_CONVEYOR_BELT = False
        self.TURN_ON_RED_LED = False
        self.TURN_ON_GREEN_LED = False
        self.TURN_ON_BLINKING_RED_LED = False
        self.TURN_ON_CAM_LED = False
        self.TURN_OFF_CAM_LED = False


        self.GET_WEIGHT = False
        self.TARE_STATUS = False
        self.TARE_VALUE = 0
        
        

        _thread.start_new_thread(cf.check_connected_devices_worker,(self,))
       
        # while not (self.STM32_STATUS and self.PRINTER_STATUS and self.SCANNERS_STATUS):
            # print(c.WARNING+"Communication class: Waiting for devices to connect..."+c.ENDC)
            # time.sleep(1)
        print("Communication class: All devices connected, starting reading and writing threads...")



        _thread.start_new_thread(cf.STM32_communication_buffor,(self,))
        _thread.start_new_thread(cf.scanners_communication_buffor,(self,))
        _thread.start_new_thread(cf.barcodes_timer_worker,(self,))
        _thread.start_new_thread(cf.receive_communication_buffor,(self,))
        _thread.start_new_thread(cf.frontend_communication_buffor,(self,))
        
        while not self.TARE_STATUS:
            print(c.WARNING+"Communication class: Waiting for tare to be done..."+c.ENDC)
            time.sleep(2)
            self.get_weight()






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
    def tare(self):
        self.TARE_STATUS = True
    def turn_on_cam_led(self):
        self.TURN_ON_CAM_LED = True
    def turn_off_cam_led(self):
        self.TURN_OFF_CAM_LED = True
    def turn_on_blinking_red_led(self):
        self.TURN_ON_BLINKING_RED_LED = True


class synchronization():
    def __init__(self,machine_class,communication_class):
        
        print("Synchronization class: Initializing...")
        self.machine = machine_class
        self.communication = communication_class

        if not sf.validate_bottles_table():
            self.machine.STATE_SAFE_MODE = True


        _thread.start_new_thread(sf.synchronization_worker,(self,))
        #_thread.start_new_thread(sf.update_information_worker,(self,))

        print(c.OK_GREEN+"Synchronization class: Initialized!"+c.ENDC)