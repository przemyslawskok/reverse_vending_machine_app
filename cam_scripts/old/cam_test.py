import cv2
import numpy as np


camera = cv2.VideoCapture(0)


while True:
    ret, image = camera.read()
    #image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    cv2.imshow('', image)
    # image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    # image = (image / 127.5) - 1
    keyboard_input = cv2.waitKey(1)
    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()
