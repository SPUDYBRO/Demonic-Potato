import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from discord.app_commands import Choice
import dblogger
from dblogger import *
import random




bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), api_version=9)

DemonicMuck = 856433605157191680


token, test_token = dblogger.tokengrabber()

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
        print("Bot Ready!")
    except Exception as e:
        print(e)

@bot.event
async def on_guild_join(Server):
    ServerID = Server.id
    UserID = None
    await dblogger.dbfixer(UserID, ServerID)


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    UserID = message.author.id
    ServerID = message.guild.id
    await dblogger.dbfixer(UserID, ServerID)

@bot.event
async def on_member_join(member):
    UserID = member.author.id
    ServerID = member.guild.id
    await dblogger.dbfixer(UserID, ServerID)




@bot.tree.command(name="counter", description="how many commands or messages have you used")
@app_commands.choices(
    choice=[
        Choice(name="Messages Sent", value="msg"),
        Choice(name="Commands Used", value="cmd"),
        Choice(name="Server Total", value="total")
    ]
)
async def counter(interaction: discord.Interaction, choice: str):
    UserID = interaction.user.id
    ServerID = interaction.guild_id
    await dblogger.cmdcountup(UserID, ServerID)
    counted, counted2 = await dblogger.countergrabber(UserID, ServerID, choice)
    print (UserID, choice, counted)
    if choice == 'msg':
        await interaction.response.send_message(f"Messages sent: **{counted}**")
    elif choice == 'cmd':
        await interaction.response.send_message(f"Commands Used: **{counted}**")
    elif choice == 'total':
        await interaction.response.send_message(f"Total messages in server: **{counted}**\nTotal Commands Used in server: **{counted2}**")
    else:
        await interaction.response.send_message(f"not valid choice")
        print (f"{UserID} has used {choice} as a choice in counter command. it is invalid")



@bot.tree.command(name="repeat")
@app_commands.describe(message="message")
async def say(interaction: discord.Interaction, message: str):
    UserID = interaction.user.id
    ServerID = interaction.guild_id
    await dblogger.msgcountup(UserID, ServerID)
    await dblogger.cmdcountup(UserID, ServerID)
    if ServerID == DemonicMuck:
        print('repeat used in main server')
        nwordfound = await dblogger.slurselect(message)
        if nwordfound:
            await interaction.response.send_message(f"{interaction.user.mention} is a pedophile")
        else:
            await interaction.response.send_message(message)
    else:
        innapropiate = await dblogger.flaggedwords(message, ServerID, UserID)
        if innapropiate:
            await interaction.response.send_message("Sorry, that message contains forbidden words.", ephemeral=True)
        else:
            await interaction.response.send_message(message)


@bot.tree.command(name="warn", description="Adds a warning to a user")
async def warn_command(interaction: discord.Interaction, user: discord.Member, reason: str):
    WarnedID = user.id
    UserID = interaction.user.id
    ServerID = interaction.guild_id
    Timestamp = datetime.now().strftime("%Y-%m-%d")
    EventID = await dblogger.generate_event_id(8)
    await dblogger.cmdcountup(UserID, ServerID)
    Success = await dblogger.warnlogger(UserID, ServerID, Timestamp, WarnedID, EventID, reason)
    if Success:
        await interaction.response.send_message(f"{user.mention} has been warned for {reason}")
    else:
        await interaction.response.send_message("Failed to warn user")

    


@bot.tree.command(name="kick", description="Kicks a user")
async def kick_command(interaction: discord.Interaction, user: discord.Member, *, reason: str = "No reason provided."):
    WarnedID = user.id
    UserID = interaction.user.id
    ServerID = interaction.guild_id
    Timestamp = datetime.now().strftime("%Y-%m-%d")
    await dblogger.cmdcountup(UserID, ServerID)
    
     # Log the kick action
    success = await dblogger.kicklogger(UserID, ServerID, Timestamp, WarnedID, reason)
    if success:
        await user.kick(reason=reason)
        await interaction.response.send_message(f"{user.mention} has been kicked for {reason}")
    else:
        await interaction.response.send_message("Failed to log kick action")
        





@bot.tree.command(name="actionlist", description="Shows a list of actions afflicted on a user")
@app_commands.choices(
    type=[
        Choice(name="Warns", value="Warn"),
        Choice(name="Kicks", value="Kick"),
    ]
)
async def actionlist(interaction: discord.Interaction, user: discord.Member, *, type: str):
    UserID = user.id
    UserName = user
    cmdused = interaction.user.id
    ServerID = interaction.guild_id
    await dblogger.cmdcountup(UserID, ServerID)
    embed = await dblogger.Actionlistpull(UserID, ServerID, cmdused, type, UserName)
    await interaction.response.send_message(embeds=embed)

async def disable_buttons(self):
        for child in self.children:
            child.disabled = True

class RPSbuttons(discord.ui.View):
    def __init__(self, player1, player2, p1choice):
        super().__init__(timeout=120)
        self.data = []
        self.player1 = player1
        self.player2 = player2
        self.p1choice = p1choice


    @discord.ui.button(label='rock', style=discord.ButtonStyle.green, custom_id='rock_button')
    async def rock(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"rps button rock has been used by {self.player2}")
        if interaction.user == self.player2:
            print("correct player")
            p2choice = "rock"
            #run RPS logic
            Winner = await dblogger.RPSlogic(self.player1, self.player2, self.p1choice, p2choice)
            if Winner == self.player1:
                await interaction.response.send_message(f"**{self.player1.display_name} Has Won!**\n{self.player1.display_name} chose {self.p1choice}\n{self.player2.display_name} chose {p2choice}")
                self.stop()
            if Winner == self.player2:
                await interaction.response.send_message(f"**{self.player2.display_name} Has Won!**\n{self.player1.display_name} chose {self.p1choice}\n{self.player2.display_name} chose {p2choice}")
                self.stop()
            elif Winner == "null":
                await interaction.response.send_message(f"**Its a tie!**\n{self.player1.display_name} and {self.player2.display_name} chose {self.p1choice}")
                self.stop()
        else:
            await interaction.response.send_message(f"You are the challenged one", ephemeral=True)
    
    @discord.ui.button(label='paper', style=discord.ButtonStyle.green, custom_id='paper_button')
    async def paper(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.player2:
            print("correct player")
            p2choice = "paper"
            #run RPS logic
            Winner = await dblogger.RPSlogic(self.player1, self.player2, self.p1choice, p2choice)
            if Winner == self.player1:
                await interaction.response.send_message(f"**{self.player1.display_name} Has Won!**\n{self.player1.display_name} chose {self.p1choice}\n{self.player2.display_name} chose {p2choice}")
            if Winner == self.player2:
                await interaction.response.send_message(f"**{self.player2.display_name} Has Won!**\n{self.player1.display_name} chose {self.p1choice}\n{self.player2.display_name} chose {p2choice}")
            elif Winner == "null":
                await interaction.response.send_message(f"**Its a tie!**\n{self.player1.display_name} and {self.player2.display_name} chose {self.p1choice}")
        else:
            await interaction.response.send_message(f"You are the challenged one", ephemeral=True)
        await RPSbuttons(interaction)
    
    @discord.ui.button(label='scissors', style=discord.ButtonStyle.green, custom_id='scissors_button')
    async def scissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.player2:
            print("correct player")
            p2choice = "scissors"
            #run RPS logic
            Winner = await dblogger.RPSlogic(self.player1, self.player2, self.p1choice, p2choice)
            if Winner == self.player1:
                await interaction.response.send_message(f"**{self.player1.display_name} Has Won!**\n{self.player1.display_name} chose {self.p1choice}\n{self.player2.display_name} chose {p2choice}")
            if Winner == self.player2:
                await interaction.response.send_message(f"**{self.player2.display_name} Has Won!**\n{self.player1.display_name} chose {self.p1choice}\n{self.player2.display_name} chose {p2choice}")
            elif Winner == "null":
                await interaction.response.send_message(f"**Its a tie!**\n{self.player1.display_name} and {self.player2.display_name} chose {self.p1choice}")
        else:
            await interaction.response.send_message(f"You are the challenged one", ephemeral=True)
        await RPSbuttons(interaction)
        

@bot.tree.command(name="rps", description="Play a game of RPS with a bot or a friend")
@app_commands.choices(
    choice=[
        Choice(name="Rock", value="rock"),
        Choice(name="Paper", value="paper"),
        Choice(name="Scissors", value="scissors")
    ]
)
async def RPScommand(interaction: discord.Interaction, challenged: discord.Member, *, choice: str):
    UserID = interaction.user.id
    ServerID = interaction.guild.id
    await dblogger.cmdcountup(UserID, ServerID)
    player1 = interaction.user
    player2 = challenged
    p1choice = choice


    if player2.bot: #check if they are a bot
        print(f"{player1} is fighting a bot")
        botoptions = ['rock', 'paper', 'scissors']
        p2choice = random.choice(botoptions)
        print(f"the bot chose {p2choice}")
        #Run RPS logic for the winner of the bot
        Winner = await dblogger.RPSlogic(player1, player2, p1choice, p2choice)
        if Winner == "player1":
            await interaction.response.send_message(f"**{player1.display_name} Has Won!**\n{player1.display_name} chose {p1choice}\n{player2.display_name} chose {p2choice}")
        if Winner == "player2":
            await interaction.response.send_message(f"**{player2.display_name} Has Won!**\n{player1.display_name} chose {p1choice}\n{player2.display_name} chose {p2choice}")
        elif Winner == "null":
            await interaction.response.send_message(f"**Its a tie!**\n{player1.display_name} and {player2.display_name} chose {p1choice}")
    
    elif player1 == player2: #check if they are the same person
        await interaction.response.send_message(f"Sorry you cant challenge yourself", ephemeral=True)


    else: #play against human
        print(f"{player1} is fighting {player2}")
        await interaction.response.send_message(f"{challenged.mention} you have been challenged\nchoose your weapon:", view=RPSbuttons(player1, player2, p1choice))


#run bot

# !! Change test_token to token BEFORE LAUNCH !!
bot.run(test_token)