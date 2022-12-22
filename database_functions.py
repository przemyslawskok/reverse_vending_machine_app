import sqlite3




def get_bottle_information(barcode):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BOTTLES WHERE BARCODE = ?",(barcode,))
    bottle = cursor.fetchone()
    conn.close()
    if bottle is None:
        return False
    else:
        return bottle