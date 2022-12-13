import serial.tools.list_ports
import usb_config as config
import time

def STM32_communication_buffor(communication_class):
    #Estabilish connection
    print("Establishing connection with STM32...")
    try:
        com_port=check_com_port(config.USB_VID_PID["STM32"]["VID"],config.USB_VID_PID["STM32"]["PID"])
        print("STM32 connected on port: "+com_port)
        serial_port=serial.Serial(com_port,config.USB_BAUD_RATES["STM32"]["BAUD_RATE"])
    except:
        print(">>>>>>>>>>  Error while connecting to STM32!")


    while True:
        #serial_port.write(b"A\n")
        #READ DATA FROM STM32
        if serial_port.in_waiting > 0:
            
            command = serial_port.readline()
            print(command)
        #WRITE DATA TO STM32
        # ify..







def check_com_port(VID,PID):
    ports=serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == int(VID) and port.pid == int(PID):
            return port.device
    return False
def check_connected_devices_worker(communication_class):
    while True:
        print("Checking connected devices...")
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
            if port.vid == int(config.USB_VID_PID["BARCODE_SCANNER"]["VID"]) and port.pid == int(config.USB_VID_PID["BARCODE_SCANNER"]["PID"]):
                number_of_scanners += 1
        if number_of_scanners == 6:
            communication_class.SCANNERS_STATUS = True
        else:
            communication_class.SCANNERS_STATUS = False

        time.sleep(2)
        

