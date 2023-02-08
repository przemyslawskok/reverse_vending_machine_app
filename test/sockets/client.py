import socket            
import time

while True:
    s = socket.socket()        
    port = 12345               
    s.connect(('127.0.0.1', port))
    s.send('Hello'.encode())
    time.sleep(1)