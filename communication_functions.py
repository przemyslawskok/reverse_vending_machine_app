import serial.tools.list_ports
import usb_config as config
import time
import _thread
from syntax import colors as c

def STM32_communication_buffor(communication_class):
    #Estabilish connection
    print("Communication class: Establishing connection with STM32...")
    try:
        com_port=check_com_port(config.USB_VID_PID["STM32"]["VID"],config.USB_VID_PID["STM32"]["PID"])
        serial_port=serial.Serial(com_port,config.USB_BAUD_RATES["STM32"]["BAUD_RATE"])
        print("Communication class: STM32 connected on port: "+com_port)
    except:
        print(c.ERROR+"Communication class: Error while connecting to STM32!"+c.ENDC)
        print(c.ERROR+"Communication class: Aborting STM32_communication_buffor()"+c.ENDC)
        communication_class.STM32_STATUS = False
        return

    print(c.OK_GREEN+"Communication class: STM32 connection estabilished!"+c.ENDC)

    # serial_port.write(b"B\n")
    while True:
        #READ DATA FROM STM32
        
       
        #WRITE DATA TO STM32
        # ify..

        if communication_class.ASK_SENSOR_IN_HOLE:
            print(c.OK_BLUE+"Communication class: Asking STM32 if sensor in hole..."+c.ENDC)
            serial_port.write(b"F\n")
            communication_class.ASK_SENSOR_IN_HOLE = False
        elif communication_class.TURN_ON_CONVEYOR_BELT_FORWARD:
            print(c.OK_BLUE+"Communication class: Asking STM32 if sensor in hole..."+c.ENDC)
            serial_port.write(b"A\n")
            communication_class.TURN_ON_CONVEYOR_BELT_FORWARD = False
        elif communication_class.TURN_ON_CONVEYOR_BELT_BACKWARD:
            print(c.OK_BLUE+"Communication class: Asking STM32 if sensor in hole..."+c.ENDC)
            serial_port.write(b"B\n")
            communication_class.TURN_ON_CONVEYOR_BELT_BACKWARD = False
        elif communication_class.TURN_OFF_CONVEYOR_BELT:
            print(c.OK_BLUE+"Communication class: Asking STM32 if sensor in hole..."+c.ENDC)
            serial_port.write(b"C\n")
            communication_class.TURN_OFF_CONVEYOR_BELT = False

        if serial_port.in_waiting > 0:
                    command = serial_port.readline()
                    print(command)
                
        
        

def scanners_communication_buffor(communication_class):
    print("Communication class: Establishing connection with scanners...")
    #get list of com ports of scanners
    scanners_com_ports=check_scanners_com_ports()
    if scanners_com_ports:
        for com_port in scanners_com_ports:
            _thread.start_new_thread(read_scanner_data,(com_port,communication_class))

            

def read_scanner_data(com_port, communication_class):
    try:
        serial_port=serial.Serial(com_port,config.USB_BAUD_RATES["SCANNER"]["BAUD_RATE"])
        print(c.OK_GREEN+"Communication class: Scanner connected on port: "+com_port+c.ENDC)
    except:
        print(c.ERROR+"Communication class: Error while connecting to scanner on port: "+str(com_port)+c.ENDC)
        print(c.ERROR+"Communication class: Aborting read_scanner_data() with port: "+str(com_port)+c.ENDC)
        return
    while True:
        if serial_port.in_waiting > 0:
            try:
                barcode = serial_port.readline().decode("utf-8").strip()
                #Check if barcode is 11 characters long
                if len(barcode) == 13:
                    communication_class.BARCODES.append(barcode)
                    communication_class.BARCODES_TIMER=20
                    print("Communication class: Barcode scanned on port: "+com_port+" with value: "+str(barcode))
                else:
                    print(c.WARNING+"Communication class: Invalid barcode scanned on port: "+com_port+" with value: "+str(barcode)+c.ENDC)
            except:
                print(c.WARNING+"Communication class: Can't decode data from scanner on port: "+str(com_port)+c.ENDC)


def barcodes_timer_worker(communication_class):
    print(c.OK_GREEN+"Communication class: Barcodes timer worker started!"+c.ENDC)
    while True:
        if communication_class.BARCODES_TIMER>0:
            communication_class.BARCODES_TIMER-=1
            time.sleep(0.1)
        elif communication_class.BARCODES_TIMER==0:

            communication_class.BARCODES_TIMER= -1
            communication_class.BARCODES=[]
            print("Communication class: Barcodes timer expired!")



def check_scanners_com_ports():
    ports=serial.tools.list_ports.comports()
    scanners_com_ports=[]
    for port in ports:
        if port.vid == int(config.USB_VID_PID["SCANNER"]["VID"]) and port.pid == int(config.USB_VID_PID["SCANNER"]["PID"]):
            scanners_com_ports.append(port.device)
    if len(scanners_com_ports) < config.NUMBER_OF_SCANNERS:
        print(c.ERROR+"Communication class: No scanners connected!"+c.ENDC)
        return False
    return scanners_com_ports

def check_com_port(VID,PID):
    ports=serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == int(VID) and port.pid == int(PID):
            return port.device
    return False
def check_connected_devices_worker(communication_class):
    print(c.OK_GREEN+"Communication class: Check connected devices worker started!"+c.ENDC)
    while True:
        #Download list of connected devices
        ports=serial.tools.list_ports.comports()
        #Check if STM32 is connected
        for port in ports:
            if port.vid == int(config.USB_VID_PID["STM32"]["VID"]) and port.pid == int(config.USB_VID_PID["STM32"]["PID"]):
                communication_class.STM32_STATUS = True
                break
            else:
                communication_class.STM32_STATUS = False

        #Check if thermal printer is connected
        for port in ports:
            if port.vid == int(config.USB_VID_PID["THERMAL_PRINTER"]["VID"]) and port.pid == int(config.USB_VID_PID["THERMAL_PRINTER"]["PID"]):
                communication_class.PRINTER_STATUS = True
                break
            else:
                communication_class.PRINTER_STATUS = False

        #Check if six barcode scanners are connected
        number_of_scanners = 0 
        for port in ports:
            if port.vid == int(config.USB_VID_PID["SCANNER"]["VID"]) and port.pid == int(config.USB_VID_PID["SCANNER"]["PID"]):
                number_of_scanners += 1
        if number_of_scanners == 6:
            communication_class.SCANNERS_STATUS = True
        else:
            communication_class.SCANNERS_STATUS = False

        # if communication_class.STM32_STATUS == False or communication_class.PRINTER_STATUS == False or communication_class.SCANNERS_STATUS == False:
            
        #     print(c.WARNING+"Communication class: No all devices connected!"+c.ENDC)
        time.sleep(1)
        

