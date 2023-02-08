#read txt file 
import random
#from keras.models import load_model

f = open("test.txt", "w+")
counter = 0
while True:
    list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    string = ''
    for x in list:
        string += x

    f.write("abcdefghijklmnopqrstuvwxyz")
    #write random number to file
    counter = counter + 1
    if counter == 2:
        #clear file
        f.truncate(0)
        counter = 0
f.close()