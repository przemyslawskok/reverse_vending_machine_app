from keras.models import load_model
import cv2
import _thread
from time import time,sleep
from concurrent.futures import ThreadPoolExecutor

CAMERA_UP = cv2.VideoCapture(0)
CAMERA_LID = cv2.VideoCapture(1)

def gcd(a):
    print('start')
    MODEL_UP = load_model('functions/ml_files/model_up.h5')
    MODEL_LID = load_model('functions/ml_files/model_lid.h5')

    print('end')
    return MODEL_UP, MODEL_LID

start = time()
pool = ThreadPoolExecutor(max_workers=10)
results = list(pool.map(gcd,('a'))
end = time()
print('Operacja zabrađa %.3f sekund' % (end - start))

while True:
    sleep(1)
    print(results)
    continue

# import pp
# job_server = pp.Server() 


# CAMERA_UP = cv2.VideoCapture(0)
# CAMERA_LID = cv2.VideoCapture(1)


# def stress_test():
#     x = 11221
#     while True:
#         x*x
#     #do a stress test


# job1 = job_server.submit(stress_test, ())
# job2 = job_server.submit(stress_test, ())


# def do_job():
#     job1()
#     job2()
# _thread.start_new_thread(do_job, ())
# # _thread.start_new_thread(stress_test, ())
# # _thread.start_new_thread(stress_test, ())
# # _thread.start_new_thread(stress_test, ())

# print('przed')
# MODEL_UP = load_model('functions/ml_files/model_up.h5')
# MODEL_LID = load_model('functions/ml_files/model_lid.h5')
# print("po")

# while True:
#     continue