
import socket            
 
s = socket.socket()        
print ("Socket successfully created")
 
port = 12345               

s.bind(('127.0.0.1', port))        
print ("socket binded to %s" %(port))
 
# put the socket into listening mode
s.listen(5)    
print ("socket is listening")           

while True:

    c, addr = s.accept()    
    print ('Got connection from', addr )

    data = c.recv(1024)

    print(data)
    c.close()
 