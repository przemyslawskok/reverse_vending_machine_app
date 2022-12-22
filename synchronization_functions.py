import sqlite3
from syntax import colors as c
import time


def synchronization_worker(synchronization_class):
    print("Synchronization class: Starting synchronization worker...")
    while True:
        time.sleep(1)
        #check if is something new in database
        
        continue
def update_information_worker(synchronization_class):
    print("Synchronization class: Starting update information worker...")
    while True:

        continue
def validate_bottles_table():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM BOTTLES")
        conn.close()
    except:
        print(c.WARNING + "Synchronization class: Table 'BOTTLES' not found! Creating one.." + c.ENDC)
        # try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE BOTTLES
        (ID INTEGER PRIMARY KEY,
        BARCODE TEXT,
        NAME TEXT,
        MATERIAL TEXT,
        WEIGHT INTEGER)""")
        conn.commit()
        conn.close()

        # except:
        #     print(c.ERROR + "Synchronization class: Failed to create table 'BOTTLES'! Aborting validate_bottles_table()" + c.ENDC)
        #     return False






