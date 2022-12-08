import _thread

class machine():

    def __init__(self):
        self.STARTING_SEQUENCE = False      
        self.CONVEYOUR_BELT = False         #F - Forward, B - Backward, False - Stop
        self.RING_SENSOR = False            #True - Object in ring detected, False - Ring empty
        self.VALVE_SENSOR = False           #True - Object near valve, False - No object near valve
        self.PRINTER_SPOOL = 0              #Integer - Number of % of spool left
        self.BIN_FILLING_LEVEL = 0          #Integer - Number of % of bin filling level


class communication():
    def __init__(self,machine_class):
        self.machine = machine_class

class communication():
    def __init__(self,machine_class):
        self.machine = machine_class

class communication():
    def __init__(self,machine_class):
        self.machine = stm32