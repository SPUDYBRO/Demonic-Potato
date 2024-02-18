import sqlite3

# Connect to the database (creates a new file if it doesn't exist)
conn = sqlite3.connect('Data/Servers/')

# Create a cursor object to execute SQL statements
cursor = conn.cursor()

# Execute SQL statements to create tables
cursor.execute('''
        CREATE TABLE "Mod Actions" (
	        "UserID"	INTEGER,
	        "EventID"	INTEGER,
	        "Action"	TEXT,
	        "Reason"	TEXT,
	        "Timestamp"	TEXT,
	        "ModID"	INTEGER
        );
    ''')
cursor.execute('''
        CREATE TABLE "Userinfo" (
            "UserID" INTEGER,
            "XP" INTEGER,
            "SA" INTEGER,
            "msgsent" INTEGER,
            "Cmdused" INTEGER
        )
    ''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database created successfully!")





# this program is to make databases manualy