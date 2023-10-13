import sqlite3
import os
import asqlite
import discord
from datetime import datetime
import string
import random



# Function to generate an event ID
async def generate_event_id(length):
    characters = string.ascii_letters + string.digits
    EventID = ''.join(random.choice(characters) for _ in range(length))
    return EventID

# Get tokens
def tokengrabber():
    connection = sqlite3.connect('Data/tokens.db')
    db = connection.cursor()

    db.execute('''SELECT token FROM tokens WHERE id = 1 OR id = 2''')
    tokens = db.fetchall()

    token = tokens[0][0]
    test_token = tokens[1][0]
    return token, test_token












async def dbfixer(UserID, ServerID):
    #check if server file exists
    server_file = f'Data/Servers/{ServerID}.db'
    if os.path.exists(server_file):
        print(f"server file {ServerID}.db found")
        if UserID:
            print("User ID collected")
            #check if the user has a spot in the database if not create one

            db = await asqlite.connect(f"Data/Servers/{ServerID}.db")
            cursor = await db.cursor()

            # Check if the user ID already exists in the table
            await cursor.execute('''SELECT UserID FROM Userinfo WHERE UserID = ?''', (UserID,))
            existing_user = await cursor.fetchone()

            if existing_user is None:
                print(f"user does not exist. inserting")
                # Insert the user ID if it doesn't exist yet
                await cursor.execute('''INSERT INTO Userinfo (UserID, XP, SA, msgsent, Cmdused) VALUES (?, 0, 0, 0, 0)''', (UserID,))
                await db.commit()
                await db.close()
                print(f"{UserID} added to db {ServerID}.db")
            else:
                print(f"user exists. skipping")
                await db.close()
        else:
            print(f"no UserID variable input (set to None)")

    else:
        print(f"no server file located. creating...")
        #create server file for the server

        # Create a new SQLite Database for the server
        db = await asqlite.connect(server_file)
        cursor = await db.cursor()

        # Create the necessary tables in the new Database
        await cursor.execute('''
            CREATE TABLE "Mod Actions" (
                "UserID"    INTEGER,
                "EventID"   INTEGER,
                "Action"    TEXT,
                "Reason"    TEXT,
                "Timestamp" TEXT,
                "ModID"     INTEGER
            );
        ''')
        await cursor.execute('''
            CREATE TABLE "Userinfo" (
                "UserID"   INTEGER,
                "XP"       INTEGER,
                "SA"       INTEGER,
                "msgsent"  INTEGER,
                "Cmdused"  INTEGER
            )
        ''')

        # Commit changes and close the Database db
        await db.commit()
        await db.close()
        print(f"server File created:  {ServerID}.db")



async def msgcountup(UserID, ServerID):
    db = await asqlite.connect(f"Data/Servers/{ServerID}.db")
    cursor = await db.cursor()
    await cursor.execute('''UPDATE Userinfo SET msgsent = msgsent + 1 WHERE UserID = ?''', (UserID,))
    print(f"message count upped for {UserID} in server {ServerID}")
    await db.commit()
    await db.close()


async def cmdcountup(UserID, ServerID):
    await dbfixer(UserID, ServerID)
    db = await asqlite.connect(f"Data/Servers/{ServerID}.db")
    cursor = await db.cursor()
    await cursor.execute('''UPDATE Userinfo SET Cmdused = Cmdused + 1 WHERE UserID = ?''', (UserID,))
    print(f"command count upped for {UserID} in server {ServerID}")
    await db.commit()
    await db.close()



async def warnlogger(UserID, ServerID, Timestamp, WarnedID, EventID, reason):
    try:
        await dbfixer(UserID, ServerID)
        db = await asqlite.connect(f"Data/Servers/{ServerID}.db")
        cursor = await db.cursor()
        await cursor.execute('''INSERT INTO "Mod Actions" (UserID, EventID, Action, Reason, Timestamp, ModID) VALUES (?, ?, ?, ?, ?, ?)''', (WarnedID, EventID, "Warn", reason, Timestamp, UserID))
        await db.commit()
        await db.close()
        Success = True
    except discord.errors.NotFound:
        Success = False
    return Success


async def kicklogger(UserID, ServerID, Timestamp, WarnedID, reason):
    try:
        await dbfixer(UserID, ServerID)
        EventID = await generate_event_id(8)
        db = await asqlite.connect(f"Data/Servers/{ServerID}.db")
        cursor = await db.cursor()
        await cursor.execute('''INSERT INTO "Mod Actions" (UserID, EventID, Action, Reason, Timestamp, ModID) VALUES (?, ?, ?, ?, ?, ?)''',(WarnedID, EventID, "Kick", reason, Timestamp, UserID))
        await db.commit()
        await db.close()
        success = True
    except discord.errors.NotFound:
        success = False
    return success






async def Actionlistpull(UserID, ServerID, cmdused, type, UserName):
    await dbfixer(UserID, ServerID)
    db = await asqlite.connect(f"Data/Servers/{ServerID}.db")
    cursor = await db.cursor()
    server_file = f'Data/Servers/{ServerID}.db'
    if not os.path.exists(server_file):
        return
    
    if type == "Warn":
        await cursor.execute('''SELECT UserID, EventID, Reason, Timestamp, ModID FROM "Mod Actions" WHERE UserID = ? AND Action = ?''', (UserID, type))
        rows = await cursor.fetchall()
        await db.commit()
        await db.close()

        embeds = []
        if rows:
            count = len(rows)
            for i, row in enumerate(rows):
                event_id = row[1]
                reason = row[2]
                timestamp = row[3]
                mod_id = row[4]

                embed = discord.Embed(color=discord.Color.gold())
                if i == 0:
                    embed.title = f"List of warns for {UserName.name}"
                else:
                    embed.title = f"Warn {i+1} for {UserName.name}"
                embed.add_field(name="Moderator ID:", value=f"<@{mod_id}>", inline=False)
                embed.add_field(name="Reason:", value=reason, inline=False)
                embed.add_field(name="ID:", value=event_id, inline=False)
                embed.add_field(name="Date:", value=timestamp, inline=False)

                embeds.append(embed)
                
        else:
            embed = discord.Embed(color=discord.Color.gold())
            embed.add_field(name=f"No Warns for {UserName.name}", value="No warns found for the user.")
            embeds.append(embed)

        return embeds


    elif type == "Kick":
        await cursor.execute('''SELECT UserID, EventID, Reason, Timestamp, ModID FROM "Mod Actions" WHERE UserID = ? AND Action = ?''', (UserID, type))
        rows = await cursor.fetchall()
        await db.commit()
        await db.close()

        embeds = []
        if rows:
            count = len(rows)
            for i, row in enumerate(rows):
                event_id = row[1]
                reason = row[2]
                timestamp = row[3]
                mod_id = row[4]

                embed = discord.Embed(color=discord.Color.gold())
                if i == 0:
                    embed.title = f"List of kicks for {UserName.name}"
                else:
                    embed.title = f"kick {i+1} for {UserName.name}"
                embed.add_field(name="Moderator ID:", value=f"<@{mod_id}>", inline=False)
                embed.add_field(name="Reason:", value=reason, inline=False)
                embed.add_field(name="ID:", value=event_id, inline=False)
                embed.add_field(name="Date:", value=timestamp, inline=False)

                embeds.append(embed)
                
        else:
            embed = discord.Embed(color=discord.Color.gold())
            embed.add_field(name=f"No kicks for {UserName.name}", value="No kicks found for the user.")
            embeds.append(embed)

        return embeds


    


#badwordchecker

async def flaggedwords(message, ServerID, User):
    db = await asqlite.connect(f"Data/wordfilter.db")
    cursor = await db.cursor()
    await cursor.execute('''SELECT Word FROM FlaggedWords''')
    forbidden_words = await cursor.fetchall()
    for word in forbidden_words:
        if word[0].lower() in message.lower():
            innapropiate = True
            return innapropiate
    innapropiate = False
    return innapropiate


async def slurselect(message):
    db = await asqlite.connect(f"Data/wordfilter.db")
    cursor = await db.cursor()
    await cursor.execute('''SELECT Word FROM FlaggedWords WHERE WordID IN (36, 37)''')
    badwords = await cursor.fetchall()
    for badword in badwords:
        if badword[0].lower() == message.lower():
            return True
    return False

async def countergrabber(UserID, ServerID, choice):
    await dbfixer(UserID, ServerID)
    db = await asqlite.connect(f"Data/Servers/{ServerID}.db")
    cursor = await db.cursor()
    if choice == 'msg':
        print (f"sent message count in server {ServerID} by {UserID}")
        await cursor.execute('''SELECT msgsent FROM Userinfo WHERE UserID = ?''', UserID)
        result = await cursor.fetchone()
        counted = result[0]
        counted2 = None
        return counted, counted2
    elif choice == 'cmd':
        print (f"sent command count in server {ServerID} by {UserID}")
        await cursor.execute('''Select Cmdused FROM Userinfo WHERE UserID = ?''', UserID)
        result= await cursor.fetchone()
        counted = result[0]
        counted2 = None
        return counted, counted2
    elif choice == 'total':
        print(f"Calculating total sent messages in server {ServerID} by {UserID}")
        await cursor.execute('''SELECT msgsent FROM Userinfo''')
        results = await cursor.fetchall()
        counted = sum(row[0] for row in results)
        await cursor.execute('''SELECT Cmdused FROM Userinfo''')
        results2 = await cursor.fetchall()
        counted2 = sum(row[0] for row in results2)
        return counted, counted2

    await db.close


async def RPSlogic(player1, player2, p1choice, p2choice):
    # p1 rock possabilitys
    if p1choice == "rock":
        if p2choice == "rock":
            Winner = "null"
            return Winner
        elif p2choice == "scissors":
            Winner = "player1"
            return Winner
        elif p2choice == "paper":
            Winner = "player2"
            return Winner
    # p1 Paper Possabilitys
    elif p1choice == "paper":
        if p2choice == "rock":
            Winner = "player1"
            return player1
        elif p2choice == "paper":
            Winner = "null"
            return Winner
        elif p2choice == "scissors":
            Winner = "player2"
            return Winner
    # p1 Scissors Possablilitys
    elif p1choice == "scissors":
        if p2choice == "rock":
            Winner = "player2"
            return Winner
        elif p2choice == "paper":
            Winner = "player1"
            return Winner
        elif p2choice == "scissors":
            Winner = "null"
            return Winner