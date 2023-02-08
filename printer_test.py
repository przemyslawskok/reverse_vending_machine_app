
import serial


p=serial.Serial(port = "COM16", baudrate=115200,
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


p.write(b"\x1B\x64\x02")
p.write(b"To moj pierwszy paragon, witaj!")
p.write(b"\x1B\x64\x02")


    
p.write(b"-------------------------------\n")    

p.write(b"\x1B\x64\x02")
p.write(b"Ilosc poprawnych butelek: ")
p.write(b"\x1B\x64\x02")


p.write(b"\x1d\x6b\x08\x7b\x42") #init barcode
p.write(b"\x32\x32\x30\x35\x32\x32\x30\x35") #barcode value
p.write(b"\x00") #end barcode
p.write(b"\x1B\x64\x02")



p.write(b"\x1B\x64\x02")
p.write(b"Dziekuje!")
p.write(b"\x1B\x64\x02")

p.write(b"\x1D\x21\x03")   #normal height 3x width
p.write(b"-------------------------------\n")
p.write(b"\x1B\x21\x00")   #normal



p.write(b"\x1B\x64\x02") #line feed
p.write(b"\x1B\x64\x02") #line feed

p.write(b"\x1B\x69\x00")  #cut


p.close()