import _thread
import usb_config
import communication_functions as cf
import time

class machine():

    def __init__(self):
        self.STARTING_SEQUENCE = False      
        self.CONVEYOUR_BELT = False         #F - Forward, B - Backward, False - Stop
        self.RING_SENSOR = False            #True - Object in ring detected, False - Ring empty
        self.VALVE_SENSOR = False           #True - Object near valve, False - No object near valve
        self.PRINTER_SPOOL = 0              #Integer - Number of % of spool left
        self.BIN_FILLING_LEVEL = 0          #Integer - Number of % of bin filling level

class communication():a
    def __init__(self,machine_class):
        self.machine = machine_class
 
        self.STM32_STATUS = False           #True - Connected, False - Disconnected
        self.PRINTER_STATUS = False         #True - Connected, False - Disconnected
        self.SCANNERS_STATUS = False        #True - Connected, False - Disconnected


        _thread.start_new_thread(cf.check_connected_devices_worker,(self,))

        # if self.STM32_STATUS and self.PRINTER_STATUS and self.SCANNERS_STATUS:
            # print("Communication class: All devices connected, starting reading and writing threads...")
        _thread.start_new_thread(cf.STM32_communication_buffor,(self,))
kom=communication(machine())
while True:
    
    continue