import sqlite3



def get_bottle_information(barcode,machine):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BOTTLES WHERE BARCODE = ?",(barcode,))
    bottle = cursor.fetchone()
    conn.close()
    if bottle is None:
        return False
    else:
        machine.DB_NAME, machine.DB_MATERIAL, machine.DB_WEIGHT, machine.DB_SIZE, machine.DB_LENGTH = bottle[2],bottle[3],bottle[4],bottle[5],bottle[6]
        return bottle[2],bottle[3],bottle[4],bottle[5],bottle[6]