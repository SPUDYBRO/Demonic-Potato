import os
import sqlite3

# Directory where your database files are stored
directory = 'Data/Servers/'

# Loop through files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.db'):  # Make sure it's a SQLite database file
        # Connect to the database
        conn = sqlite3.connect(os.path.join(directory, filename))
        cursor = conn.cursor()
        
        # Perform your updates here
        # For example, you might want to alter tables, add new columns, etc.
        # Example:
        cursor.execute('''ALTER TABLE "ServerInfo" ADD COLUMN "NewColumn" TEXT''')
        # Or
        #cursor.execute('''
        #    CREATE TABLE IF NOT EXISTS ServerInfo (
        #        "ClearVotesFlag" TEXT
        #    )
        #''')

        #cursor.execute('''
        #    CREATE TABLE IF NOT EXISTS Votes (
        #       "Suggestion" TEXT,
        #        "UserID" INTEGER,
        #        "EventID" INTEGER,
        #        "Timestamp" TEXT
        #    )
        #''')

print("All databases updated successfully!")
