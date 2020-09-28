import sqlite3

conn = sqlite3.connect("RCWdatabase.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE RCWDB(
Name TEXT PRIMARY KEY NOT NULL,
Reports INTEGER NOT NULL,
Commends INTEGER NOT NULL,
Currency INTEGER NOT NULL);
''')

conn.commit()
