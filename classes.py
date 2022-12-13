import _thread
import usb_config
import communication_functions as cf
import time
from syntax import colors as c
class machine():

    def __init__(self):
        print("Machine class: Initializing...")
        
        
        self.STARTING_SEQUENCE = False      
        self.CONVEYOUR_BELT = False         #F - Forward, B - Backward, False - Stop
        self.RING_SENSOR = False            #True - Object in ring detected, False - Ring empty
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


        _thread.start_new_thread(cf.check_connected_devices_worker,(self,))

        while not (self.STM32_STATUS and self.PRINTER_STATUS and self.SCANNERS_STATUS):
            print(c.WARNING+"Communication class: Waiting for devices to connect..."+c.ENDC)
            time.sleep(1)
        print("Communication class: All devices connected, starting reading and writing threads...")



        _thread.start_new_thread(cf.STM32_communication_buffor,(self,))
        _thread.start_new_thread(cf.scanners_communication_buffor,(self,))



        print(c.OK_GREEN+"Communication class: Initialized!"+c.ENDC)

kom=communication(machine())
while True:
    
    continue