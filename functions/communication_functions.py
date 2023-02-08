import serial.tools.list_ports
import functions.usb_config as config
import functions.machine_config as machine_config
import functions.machine_functions as mf
import time
import _thread
import socket
from functions.syntax import colors as c
def decode_message(message,communication_class):
    message = message.split("@")
    if message[0]=="frontend":
        print(c.OK_BLUE+"Communication class: Data received from frontend: "+ message[1] +c.ENDC)
        if message[1] == "START":
            mf.start_sequence(communication_class)
        elif message[1] == "STOP":
            mf.stop_sequence(communication_class)
    elif message[0] == "ml":
        if message[1] == "false":
            communication_class.machine.BOTTLE_PROBABILITIES = [0.00,0.00,0.00,0.00]
        else:
            if communication_class.machine.ANALYZE_UNKOWN_OBJECT:
                communication_class.machine.SET_OF_PROBABILITIES.append(message[1].split("_"))
            else:
                probabilities = message[1].split("_")
                communication_class.machine.BOTTLE_PROBABILITIES = probabilities

        if not message[2] == "false":
            communication_class.machine.BOTTLE_LENGTH = float(message[2])
     
     
        # probabilities = message[1].split("_")
        # communication_class.machine.BOTTLE_PROBABILITIES = probabilities
        # print(c.OK_BLUE+"Communication class: Data received from ML: "+ message[1] +c.ENDC)


def receive_communication_buffor(communication_class):
    s = socket.socket()
    s.bind((config.BACKEND_HOST, config.BACKEND_PORT))
    s.listen(5)
    _thread.start_new_thread(ml_update_information_worker,(communication_class,))
    print(c.OK_GREEN+"Communication class: Receive buffor estabilished!"+c.ENDC)
    while True:
        client, addr = s.accept()    
        data = client.recv(1024)
        data = data.decode()
        decode_message(data,communication_class)
        # if addr[1] == config.FRONTEND_PORT:
        #     print(c.OK_BLUE+"Communication class: Data received from frontend: "+ data +c.ENDC)
            # ml_decode_message(data,communication_class)
            # communication_class.ML_BUFFOR_UPDATE = True
        client.close()
 
def frontend_communication_buffor(communication_class):
  
    print(c.OK_GREEN+"Communication class: Frontend connection estabilished!"+c.ENDC)
    while True:
        try:
        # time.sleep(0.015)
            s = socket.socket()
            s.connect((config.FRONTEND_HOST, config.FRONTEND_PORT))

            string = ""
            string += communication_class.machine.BOTTLE_SIZE + "@"
            string += communication_class.machine.BOTTLE_MATERIAL + "@"
            string += str(communication_class.WEIGHT_VALUE) + "@"
            string += str(communication_class.machine.BOTTLE_LENGTH) + "@" 


            for key in communication_class.machine.STATES:
                if communication_class.machine.STATES[key]:
                    string += key + "@"

            # if communication_class.machine.STATE_IDLE:
            #     string += "idle@"
            # elif communication_class.machine.STATE_READY:
            #     string += "ready@"
            # elif communication_class.machine.STATE_RUNNING:
            #     string += "running@"
            # elif communication_class.machine.STATE_SAFE_MODE:
            #     string += "safe_mode@"
            # elif communication_class.machine.STATE_RUNNING_GIVING:
            #     string += "running_giving@"
            # elif communication_class.machine.STATE_WAITING_FOR_TAKE:
            #     string += "waiting_for_take@"
            # elif communication_class.machine.STATE_RUNNING_CRUSHING:
            #     string += "running_crushing@"


            if communication_class.machine.RING_SENSOR:
                string += "detected@" 
            else:
                string += "not_detected@"

            if communication_class.machine.BOTTLE_END_SENSOR:
                string += "detected@"
            else:
                string += "not_detected@"
                            
            for probability in communication_class.machine.BOTTLE_PROBABILITIES:
                string += str(probability) + " "
            string += "@"

            try:
                string += communication_class.BARCODES[-1] + "@"
            except:
                string += "none@"

            #db
            string += str(communication_class.machine.DB_SIZE) + "@"
            string += str(communication_class.machine.DB_MATERIAL) + "@"
            string += str(communication_class.machine.DB_WEIGHT) + "@"
            string += str(communication_class.machine.DB_LENGTH) + "@"
            string += str(communication_class.machine.DB_NAME) + "@"
            string += str(communication_class.machine.WEIGHT_DB_DIFFRENCE) + ""



            s.send(string.encode())
            s.close()



        except:
            print(c.ERROR+"Communication class: Frontend connection lost!"+c.ENDC)
            time.sleep(1)
def ml_decode_message(message,communication_class):
    probabilities_List = message.split("_")
    communication_class.ML_BUFFOR = probabilities_List
def ml_update_information_worker(communication_class):
    print(c.OK_GREEN+"Communication class: ML update information worker started!"+c.ENDC)
    while True:
        if communication_class.ML_BUFFOR_UPDATE:
            #check if some of the probabilities is higher than 50
            bottle = {
                "unkown" : False,
                "material": "",
                "size": "",

            }
            counter = 0
            for probability in communication_class.ML_BUFFOR:

                if float(probability) > config.ML_FACTOR and counter < 5:
                    if counter == 0:
                        bottle["material"] = "plastic"
                        bottle["unkown"] = False
                        break
                    elif counter == 1:
                        bottle["material"] =  "metal"
                        bottle["unkown"] = False
                        break
                    elif counter == 2:
                        bottle["material"] =  "glass"
                        bottle["unkown"] = False
                        break
                    elif counter == 3:
                        bottle["material"] =  "something"
                        bottle["unkown"] = True
                    elif counter == 4:
                        bottle["material"] =  "empty"
                        bottle["unkown"] = True
                counter +=1
                
            counter = 0
            for probability in communication_class.ML_BUFFOR:
                
                if counter < 5:
                    communication_class.machine.BOTTLE_PROBABILITIES[counter] = float(probability)
                    counter +=1

            if bottle["unkown"] == True:
                communication_class.ML_BUFFOR_UPDATE = False
                communication_class.machine.UNKOWN_OBJECT = True

                continue
            else:
                if float(communication_class.ML_BUFFOR[5]) > 23 :
                    bottle["size"] = "big_bottle"
                else:
                    bottle["size"] = "small_bottle"
                
                communication_class.machine.BOTTLE_LENGTH=float(communication_class.ML_BUFFOR[5])

                #save bottle to machine
                communication_class.machine.BOTTLE_MATERIAL = bottle["material"]
                communication_class.machine.BOTTLE_SIZE = bottle["size"]
                if bottle["material"] == "":
                    communication_class.machine.BOTTLE_MATERIAL = "unkown"
                    communication_class.machine.UNKOWN_OBJECT = True
                else:
                    communication_class.machine.UNKOWN_OBJECT = False
            
            communication_class.machine.CHECK_BOTTLE = True
                
            #reset the update flag
            communication_class.ML_BUFFOR_UPDATE = False
            print(c.OK_GREEN+"Communication class: ML update information worker: Bottle information updated!"+c.ENDC)



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

        
        if communication_class.TURN_ON_CONVEYOR_BELT_FORWARD:
            communication_class.TURN_ON_CONVEYOR_BELT_FORWARD = False
            print(c.OK_BLUE+"Communication class: Sending STM32 command to turn on conveyor belt forward"+c.ENDC)
            serial_port.write(b"A\n")
            
        elif communication_class.TURN_ON_CONVEYOR_BELT_BACKWARD:
            communication_class.TURN_ON_CONVEYOR_BELT_BACKWARD = False
            print(c.OK_BLUE+"Communication class: Sending STM32 command to turn on conveyor belt backward"+c.ENDC)
            serial_port.write(b"B\n")

        elif communication_class.TURN_ON_GREEN_LED:
            communication_class.TURN_ON_GREEN_LED = False
            print(c.OK_BLUE+"Communication class: Sending STM32 command to turn on green LED"+c.ENDC)
            serial_port.write(b"C\n")

        elif communication_class.TURN_ON_RED_LED:
            communication_class.TURN_ON_RED_LED = False
            print(c.OK_BLUE+"Communication class: Sending STM32 command to turn on red LED"+c.ENDC)
            serial_port.write(b"D\n")    

        elif communication_class.GET_WEIGHT:
            communication_class.GET_WEIGHT = False
            print(c.OK_BLUE+"Communication class: Sending STM32 command to get weight"+c.ENDC)
            serial_port.write(b"E\n")

        elif communication_class.TURN_OFF_CONVEYOR_BELT:
            communication_class.TURN_OFF_CONVEYOR_BELT = False
            print(c.OK_BLUE+"Communication class: Sending STM32 command to turn off conveyor belt"+c.ENDC)
            serial_port.write(b"H\n")

        elif communication_class.TURN_ON_BLINKING_RED_LED:
            communication_class.TURN_ON_BLINKING_RED_LED = False
            print(c.OK_BLUE+"Communication class: Sending STM32 command to turn on blinking red LED"+c.ENDC)
            serial_port.write(b"I\n")

        elif communication_class.TURN_ON_CAM_LED:
            communication_class.TURN_ON_CAM_LED = False
            print(c.OK_BLUE+"Communication class: Sending STM32 command to turn on CAM LED"+c.ENDC)
            serial_port.write(b"J\n")

        elif communication_class.TURN_OFF_CAM_LED:
            communication_class.TURN_OFF_CAM_LED = False
            print(c.OK_BLUE+"Communication class: Sending STM32 command to turn off CAM LED"+c.ENDC)
            serial_port.write(b"K\n")

        if serial_port.in_waiting > 0:
            command = serial_port.read(9).decode("utf-8")
            
            #check type of command by first character
            if command[0] == "f":
                #get sensor state
                state = command[1]
                if state == "1":
                    communication_class.machine.RING_SENSOR = True
                    print(c.OK_MAGENTA+"Communication class: Ring sensor state received from STM32: Object detected"+c.ENDC)
                    continue
                elif state == "0":
                    communication_class.machine.RING_SENSOR = False
                    print(c.OK_MAGENTA+"Communication class: Ring sensor state received from STM32: No object"+c.ENDC)
                    continue

            elif command[0] == "e":
                #get weight value by ending on "e" character
                value = "" 
                for character in command[1:]:
                    if character == "e":
                        break
                    elif character == "*":
                        continue
                    else:
                        value += character
                if not communication_class.TARE_STATUS:
                    communication_class.TARE_STATUS = True
                    communication_class.TARE_VALUE = int(value)
                    print(c.OK_MAGENTA+"Communication class: Tare value received from STM32: "+str(communication_class.TARE_VALUE)+c.ENDC)
                    continue

                value = int(value) - communication_class.TARE_VALUE
                value = value / machine_config.SCALE_MULTIPLIER
                communication_class.WEIGHT_VALUE = round(value,2)
                communication_class.machine.WEIGHED_BOTTLE = True
                print(c.OK_MAGENTA+"Communication class: Weight value received from STM32: "+str(value)+c.ENDC)
                
                
                continue

            if command[0] == "g":
                #get sensor state
                state = command[1]
                if state == "1":
                    communication_class.machine.BOTTLE_END_SENSOR = True
                    print(c.OK_MAGENTA+"Communication class: Bottle end sensor state received from STM32: Object detected"+c.ENDC)
                    continue
                elif state == "0":
                    communication_class.machine.BOTTLE_END_SENSOR = False
                    print(c.OK_MAGENTA+"Communication class: Bottle end sensor state received from STM32: No object"+c.ENDC)
                    continue
def scanners_communication_buffor(communication_class):
    print("Communication class: Establishing connection with scanners...")
    #get list of com ports of scanners
    scanners_com_ports=check_scanners_com_ports()
    if scanners_com_ports:
        for com_port in scanners_com_ports:
            _thread.start_new_thread(read_scanner_data,(com_port,communication_class))
    else:
        print(c.ERROR+"Communication class: Aborting scanner_communication_buffor()"+c.ENDC)
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
                # barcode = serial_port.readline().decode("utf-8").strip()
                barcode = serial_port.read(15)
           

                #Delete last two characters from barcode and convert it from bytes to string
                barcode=barcode.decode("utf-8").strip()

                #Check if 13 characters from barcode are digits
                if barcode.isdigit() and len(barcode)==13:
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
        

