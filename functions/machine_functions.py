from functions.syntax import colors as c
import functions.machine_config as config    
import serial
import functions.usb_config as usb_config
import functions.communication_functions as cf 
import functions.database_functions as db
def compare_bottle_size(bottle_weight, db_weight,machine_class):
    diffrence = abs(float(bottle_weight) - float(db_weight))
    percentage = 0
    if db_weight < 100:
        percentage = config.PERCENTAGE_OF_BOTTLE_WEIGHT_LOW
    elif db_weight < 200:
        percentage = config.PERCENTAGE_OF_BOTTLE_WEIGHT_MEDIUM
    else:
        percentage = config.PERCENTAGE_OF_BOTTLE_WEIGHT_HIGH
    try:
        diffrence = (diffrence*100)/float(db_weight)
    except:
        print(c.ERROR+"Machine class: Dividing by zero!" + c.ENDC)


    if diffrence < percentage:
        machine_class.WEIGHT_DB_DIFFRENCE="OK"
        print(c.OK_GREEN+"Machine class: Measured weight: "+ str(bottle_weight) +"g. | DB weight: " + str(db_weight) + "g." + "| Diffrence percentage:" + str(diffrence) + c.ENDC)
        return True
    else:
        machine_class.WEIGHT_DB_DIFFRENCE="False"
        print(c.ERROR+"Machine class: Measured weight: "+ str(bottle_weight) +"g. | DB weight: " + str(db_weight) + "g." + "| Diffrence percentage:" + str(diffrence) + c.ENDC)
        return False

def compare_bottle_weight(bottle_info, communication_class):
    #check if diffrence is less than 10%
    if float(bottle_info[4]) * 0.9 < communication_class.WEIGHT_VALUE < float(bottle_info[4]) * 1.1:
        print(c.OK_GREEN+"Communication class: Measured weight: "+ str(communication_class.WEIGHT_VALUE) +"g. | DB weight: " + str(bottle_info[4]) + "g." + c.ENDC)
        return True
    else:
        print(c.ERROR+"Communication class: Measured weight: "+ str(communication_class.WEIGHT_VALUE) +"g. | DB weight: " + str(bottle_info[4]) + "g." + c.ENDC)
        return False

def start_sequence(communication_class):
    communication_class.machine.change_state("STATE_READY",communication_class)
def stop_sequence(communication_class):
    communication_class.machine.change_state("STATE_SUCCESS",communication_class)


def add_bottle_to_sequence(communication_class,barcode):
    bottle_info = (communication_class.machine.DB_SIZE,
                    communication_class.machine.DB_MATERIAL,
                    communication_class.machine.DB_WEIGHT,
                    communication_class.machine.DB_LENGTH,
                    communication_class.machine.DB_NAME,
                    barcode)
    print(bottle_info)
    communication_class.machine.SEQUENCE_ARRAY.append(bottle_info)


def print_receipt(communication_class):
    p=serial.Serial(port = cf.check_com_port(usb_config.USB_VID_PID["THERMAL_PRINTER"]["VID"],usb_config.USB_VID_PID["THERMAL_PRINTER"]["PID"]), baudrate=115200,
                                    bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE)

    # p.write(b'\x1B\x61\x01')   center
    # p.write(b"\x1B\x69\x00")   cut
    # p.write(b"\x1B\x40")       reset
    # p.write(b"\x1B\x21\x00")   normal
    # p.write(b"\x1B\x21\x10")   double height
    # p.write(b"\x1B\x21\x20")   double width
    # p.write(b"\x1B\x21\x30")   double height and width
    # p.write(b"\x1B\x21\x01")   bold
    # p.write(b"\x1B\x21\x08")   underline
    # p.write(b"\x1B\x21\x80")   inverse
    # p.write(b"\x1B\x21\x00")   normal
    # p.write(b"\x1B\x64\x02")   line feed


    p.write(b'\x1B\x61\x01')   #center

    p.write(b"\x1D\x21\x03")   #normal height 3x width
    p.write(b"-------------------------------\n")
    p.write(b"\x1B\x21\x00")   #normal


    # p.write(b"\x1B\x64\x02")
    # p.write(b"To moj pierwszy paragon, witaj!")
    # p.write(b"\x1B\x64\x02")


        
    # p.write(b"-------------------------------\n")    

    i_s = 0
    i_b = 0
    names_string = ""
    for bottle in communication_class.machine.SEQUENCE_ARRAY:
        if str(bottle[0]) == "big_bottle":
            i_b += 1
        else:
            i_s += 1
        names_string += " , " +str (bottle[4]) 

    names_string = names_string[3:]

    p.write(b"-------------------------------\n")    
    p.write(b"\x1B\x64\x02")
    p.write(b"Ilosc butelek duzych: " + bytes(str(i_b),"utf-8"))
    p.write(b"\x1B\x64\x02")
    p.write(b"Ilosc butelek malych: " + bytes(str(i_s),"utf-8"))
    p.write(b"\x1B\x64\x02")
    p.write(b"Lista butelek: " + bytes(str(names_string),"utf-8"))
    p.write(b"\x1B\x64\x02")
    p.write(b"-------------------------------\n")
    
  
    # p.write(b"\x1B\x64\x02")
    # p.write(b"Rozmiar: " + bytes(str(bottle[0]),"utf-8"))
    # p.write(b"\x1B\x64\x02")
    # p.write(b"Material: " + bytes(str(bottle[1]),"utf-8"))
    # p.write(b"\x1B\x64\x02")
    # p.write(b"Waga [g]: " + bytes(str(bottle[2]),"utf-8"))
    # p.write(b"\x1B\x64\x02")
    # p.write(b"Dlugosc [g]: " + bytes(str(bottle[3]),"utf-8"))
    # p.write(b"\x1B\x64\x02")
    # p.write(b"Nazwa: " + bytes(str(bottle[4]),"utf-8"))
    # p.write(b"\x1B\x64\x02")
    # p.write(b"Kod kreskowy: " + bytes(str(bottle[5]),"utf-8"))
    # p.write(b"\x1B\x64\x02")
    # p.write(b"-------------------------------\n")

    # p.write(b"\x1B\x64\x02")
    # p.write(b"Waga:" + bytes(str(communication_class.WEIGHT_VALUE),"utf-8") + b"g")
    # p.write(b"\x1B\x64\x02")


    # p.write(b"\x1d\x6b\x08\x7b\x42") #init barcode
    # p.write(b"\x32\x32\x30\x35\x32\x32\x30\x35") #barcode value
    # p.write(b"\x00") #end barcode
    # p.write(b"\x1B\x64\x02")



    # p.write(b"\x1B\x64\x02")
    # p.write(b"Dziekuje!")
    # p.write(b"\x1B\x64\x02")

    p.write(b"\x1D\x21\x03")   #normal height 3x width
    p.write(b"-------------------------------\n")
    p.write(b"\x1B\x21\x00")   #normal



    p.write(b"\x1B\x64\x02") #line feed
    p.write(b"\x1B\x64\x02") #line feed

    p.write(b"\x1B\x69\x00")  #cut


    p.close()