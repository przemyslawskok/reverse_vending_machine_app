import serial.tools.list_ports
import functions.usb_config as config
from functions.syntax import colors as c
import _thread
import time
import sqlite3
import functions.machine_config as machine_config


class empty_bottle:
    def __init__(self):
        self.scanned = False
        self.barcode = None
        self.weight = None
        self.material = None
        self.name = None
        self.size = None
        self.length = None

bottle = empty_bottle()

def check_com_port(VID,PID):
    ports=serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == int(VID) and port.pid == int(PID):
            return port.device
    return False
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


def read_scanner_data(com_port, bottle):
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
                    bottle.scanned = True
                    bottle.barcode = barcode
                    #print("Communication class: Barcode scanned on port: "+com_port+" with value: "+str(barcode))
                else:
                    print(c.WARNING+"Communication class: Invalid barcode scanned on port: "+com_port+" with value: "+str(barcode)+c.ENDC)
            except:
                print(c.WARNING+"Communication class: Can't decode data from scanner on port: "+str(com_port)+c.ENDC)


for com_port in check_scanners_com_ports():

    _thread.start_new_thread(read_scanner_data,(com_port,bottle))


while True:
    #print("waiting for scan barcode..")
    if bottle.scanned:
        #wait for input x to get weitght
        inp = input("Enter W to get weight or number of g")
        if inp == "W":
            #connect with scale
            com_port=check_com_port(config.USB_VID_PID["STM32"]["VID"],config.USB_VID_PID["STM32"]["PID"])
            serial_port=serial.Serial(com_port,config.USB_BAUD_RATES["STM32"]["BAUD_RATE"])

            serial_port.write(b"E\n")
            time.sleep(4)
            if serial_port.in_waiting > 0:
                command = serial_port.read(9).decode("utf-8")

                if command[0] == "e":
                    #get weight value by ending on "e" character
                    value = "" 
                    for character in command[1:]:
                        if character == "e":
                            break
                        elif character == "*":
                            continue
                        else:
                            value += character


                    print(value)
                    #delete tare
                    value = int(value) - machine_config.TARE_SCALE_VALUE
                    #divide it by multipler to get grams
                    value = value / machine_config.SCALE_MULTIPLIER
                    #round it to 2 decimal places
                    bottle.weight = round(value,2)
                    #print(c.OK_MAGENTA+"Communication class: Weight value received from STM32: "+value+c.ENDC)
        else:
            bottle.weight = round(float(inp),2)
        inp = input (" P - Plastic , M - Metal , G - Glass ")
        if inp == "P":
            bottle.material = "Plastic"
        elif inp == "M":
            bottle.material = "Metal"
        elif inp == "G":
            bottle.material = "Glass"
        inp = input ("Enter name of bottle")
        bottle.name = inp

        inp = input ("Enter size of bottle [s,b]")
        if inp == "s":
            bottle.size = "small_bottle"
        elif inp == "b":
            bottle.size = "big_bottle"
        inp = input ("Enter length of bottle [cm]")
        bottle.length = round(float(inp),2)

        print(bottle.name)
        print(bottle.material)
        print(bottle.weight)
        print(bottle.barcode)
        print(bottle.size)
        print(bottle.length)
        #Insert into database
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM BOTTLES")
            conn.close()
        except:
            print(c.WARNING + "Synchronization class: Table 'BOTTLES' not found! Creating one.." + c.ENDC)
           
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE BOTTLES
            (ID INTEGER PRIMARY KEY,
            BARCODE TEXT,
            NAME TEXT,
            MATERIAL TEXT,
            WEIGHT INTEGER,
            SIZE TEXT,
            LENGTH INTEGER)""")
            conn.commit()
            conn.close()
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO BOTTLES (BARCODE, NAME, MATERIAL, WEIGHT, SIZE, LENGTH) VALUES (?,?,?,?,?,?)",(bottle.barcode,bottle.name,bottle.material,bottle.weight,bottle.size,bottle.length))
        conn.commit()
        conn.close()


            
            