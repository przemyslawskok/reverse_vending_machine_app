#read txt file 
#from keras.models import load_model

f = open("test.txt", "r+")
while True:   
    odczyt = f.read()
    dlugosc = len(odczyt)
    if dlugosc == 0:
        f = open("test.txt", "r+")
        continue
    else:
        print(odczyt)

f.close()
