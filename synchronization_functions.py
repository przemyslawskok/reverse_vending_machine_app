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
def validate_machine_table():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM MACHINE_INFORMATION")
        conn.close()
    except:
        print(c.WARNING + "Synchronization class: Table 'MACHINE_INFORMATION' not found! Creating one.." + c.ENDC)
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE MACHINE_INFORMATION 
            (ID INTEGER PRIMARY KEY,
            MACHINE_ID TEXT,
            PRZEBIEG INTEGER)""")
            conn.commit()
            conn.close()

        except:
            print(c.ERROR + "Synchronization class: Failed to create table 'MACHINE_INFORMATION'! Aborting validate_machine_table()" + c.ENDC)
            return False






