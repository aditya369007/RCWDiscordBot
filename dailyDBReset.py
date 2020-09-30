import sqlite3
import schedule
import time

def resetRCWDBCurrency():
    conn = sqlite3.connect("RCWdatabase.db")
    cursor = conn.cursor()
    cursor.execute('UPDATE RCWDB SET Currency = 10')
    conn.commit()
    conn.close()
    print("Database Reset!!")

schedule.every().day.at("06:00").do(resetRCWDBCurrency)

while True:
    schedule.run_pending()
    time.sleep(1)
