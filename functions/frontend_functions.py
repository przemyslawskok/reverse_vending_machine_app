import socket
import functions.usb_config as config
from functions.syntax import colors as c

def receive_buffor(frontend_class):
    try:
        s = socket.socket()
        s.bind((config.FRONTEND_HOST, config.FRONTEND_PORT))        
        s.listen(5)         
        print(c.OK_GREEN + "Frontend class: Receiving buffor initialized!" + c.ENDC)
    except:
        print(c.ERROR + "Frontend class: Receiving buffor failed!" + c.ENDC)
    while True:
        connection, addr = s.accept()    
        try:
            data = connection.recv(1024)
        except:
            print(c.ERROR + "Frontend class: Receiving buffor failed!" + c.ENDC)
        connection.close()
        decode_message(frontend_class,data.decode("utf-8"))
 
def decode_message(frontend_class,message):
    try:
        print(message)
        bottle = message.split("@")
        frontend_class.BOTTLE_SIZE = bottle[0]
        frontend_class.BOTTLE_MATERIAL = bottle[1]
        frontend_class.BOTTLE_WEIGHT = bottle[2]
        frontend_class.BOTTLE_LENGTH = bottle[3]
        frontend_class.MACHINE_STATE = bottle[4]
        frontend_class.MACHINE_RING_SENSOR = bottle[5]
        frontend_class.MACHINE_END_SENSOR = bottle[6]
        frontend_class.BOTTLE_PROBABILITIES = bottle[7]
        frontend_class.BOTTLE_BARCODE = bottle[8]
        frontend_class.DB_SIZE = bottle[9]
        frontend_class.DB_MATERIAL = bottle[10]
        frontend_class.DB_WEIGHT = bottle[11]
        frontend_class.DB_LENGTH = bottle[12]
        frontend_class.DB_NAME = bottle[13]
        frontend_class.WEIGHT_DIFFRENCE = bottle[14]
    except:
        print(c.ERROR + "Frontend class: Decoding message failed!" + c.ENDC)

def check_button_coordinates(x,y):
    if x > 0.64 and x < 0.77 and y > 0.57 and y < 0.66:
        send_message_to_backend("START")
        print("Button start clicked!")
    elif x > 0.64 and x < 0.77 and y > 0.70 and y < 0.77:
        send_message_to_backend("STOP")
        print("Button stop clicked!")

def send_message_to_backend(message):
    message = "frontend@" + message + "@"
    try:
        s = socket.socket()
        s.connect((config.BACKEND_HOST, config.BACKEND_PORT))
        s.send(message.encode("utf-8"))
        s.close()
        print(c.OK_GREEN + "Frontend class: Sending message to backend success!" + c.ENDC)
    except:
        print(c.ERROR + "Frontend class: Sending message to backend failed!" + c.ENDC)