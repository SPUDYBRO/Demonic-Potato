import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from discord.app_commands import Choice
from discord.ext.commands import MissingPermissions
import dblogger
from dblogger import *
import random



intents = discord.Intents.default()
intents.members = True
intents.message_content = True

description = '''Discord Bot :)'''

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

DemonicMuck = 856433605157191680
owner = 595044207190867985

token, test_token = dblogger.tokengrabber()

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@bot.event
async def on_guild_join(Server):
    ServerID = Server.id
    UserID = None
    await dblogger.dbfixer(UserID, ServerID)
    print("dbfixer ran (on_guild_join)")


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    UserID = message.author.id
    ServerID = message.guild.id
    await dblogger.dbfixer(UserID, ServerID)
    print("dbfixer ran (on_message)")
    await dblogger.msgcountup(UserID, ServerID)
    print("msgcountup ran (on_message)")

@bot.event
async def on_member_join(member):
    UserID = member.author.id
    ServerID = member.guild.id
    await dblogger.dbfixer(UserID, ServerID)
    print("dbfixer ran (on_member_join)")



@bot.tree.command(name="hello", description="Say hi to the bot")
async def hello_command(interaction: discord.Interaction):
    UserID = interaction.user.id
    ServerID = interaction.guild_id
    await dblogger.cmdcountup(UserID, ServerID,)
    greetings = ["Yo", "Sup", "Hello", "How you doin", "Nice to meet you!", "Greetings!", "Hi there!"]
    random_greeting = random.choice(greetings)
    await interaction.response.send_message(f"{random_greeting} {interaction.user.mention}", ephemeral=False)


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



@bot.tree.command(name="repeat", description="Make the bot say what you want")
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
    #Use if statement to check if user has manage messages permission
    if interaction.user.guild_permissions.manage_messages:
        EventID = await dblogger.generate_event_id(8)
        await dblogger.cmdcountup(UserID, ServerID)
        Success = await dblogger.warnlogger(UserID, ServerID, Timestamp, WarnedID, EventID, reason)
        if Success:
            await interaction.response.send_message(f"{user.mention} has been warned for {reason}")
        else:
            await interaction.response.send_message("Failed to warn user")
    else:
        await interaction.response.send_message(f"Sorry you dont have permssion to use this command", ephemeral=True)

    


@bot.tree.command(name="kick", description="Kicks a user")
async def kick_command(interaction: discord.Interaction, user: discord.Member, *, reason: str = "No reason provided."):
    WarnedID = user.id
    UserID = interaction.user.id
    ServerID = interaction.guild_id
    Timestamp = datetime.now().strftime("%Y-%m-%d")
    if interaction.user.guild_permissions.kick_members:
        await dblogger.cmdcountup(UserID, ServerID)
        # Log the kick action
        success = await dblogger.kicklogger(UserID, ServerID, Timestamp, WarnedID, reason)
        if success:
            await user.kick(reason=reason)
            await interaction.response.send_message(f"{user.mention} has been kicked for {reason}")
        else:
            await interaction.response.send_message("Failed to log kick action - Kick Failed")
    else:
        await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)
        





@bot.tree.command(name="actionlist", description="Shows a list of actions afflicted on a user")
@app_commands.choices(
    type=[
        Choice(name="Warns", value="Warn"),
        Choice(name="Kicks", value="Kick"),
    ]
)
async def actionlist(interaction: discord.Interaction, user: discord.Member, *, type: str):

    #check if user has permissions to use command
    
    UserID = user.id
    UserName = user
    cmdused = interaction.user.id
    ServerID = interaction.guild_id
    if interaction.user.guild_permissions.manage_messages:
        await dblogger.cmdcountup(UserID, ServerID)
        embed = await dblogger.Actionlistpull(UserID, ServerID, cmdused, type, UserName)
        await interaction.response.send_message(embeds=embed)
    else:
        await interaction.response.send_message("Sorry you dont have permission to use this command", ephemeral=True)

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
            # Run RPS logic
            Winner = await dblogger.rps_logic(self.player1, self.player2, self.p1choice, p2choice)
            await handle_winner(interaction ,Winner, self.p1choice, p2choice, self.player1, self.player2)
        else:
            await interaction.response.send_message(f"You are the challenged one", ephemeral=True)


    @discord.ui.button(label='paper', style=discord.ButtonStyle.green, custom_id='paper_button')
    async def paper(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.player2:
            print("correct player")
            p2choice = "paper"
            # Run RPS logic
            Winner = await dblogger.rps_logic(self.player1, self.player2, self.p1choice, p2choice)
            await handle_winner(interaction ,Winner, self.p1choice, p2choice, self.player1, self.player2)
            self.stop()
        else:
            await interaction.response.send_message(f"You are the challenged one", ephemeral=True)
            await RPSbuttons(interaction)


    @discord.ui.button(label='scissors', style=discord.ButtonStyle.green, custom_id='scissors_button')
    async def scissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.player2:
            print("correct player")
            p2choice = "scissors"
            # Run RPS logic
            Winner = await dblogger.rps_logic(self.player1, self.player2, self.p1choice, p2choice)
            await handle_winner(interaction ,Winner, self.p1choice, p2choice, self.player1, self.player2)
            self.stop()
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

    if player2.bot:  # Check if they are a bot
        print(f"{player1} is fighting a bot")
        botoptions = ['rock', 'paper', 'scissors']
        p2choice = random.choice(botoptions)
        print(f"the bot chose {p2choice}")
        # Run RPS logic for the winner of the bot
        Winner = await dblogger.rps_logic(player1, player2, p1choice, p2choice)
        await handle_winner(interaction ,Winner, p1choice, p2choice, player1, player2)
    elif player1 == player2:  # Check if they are the same person
        await interaction.response.send_message(f"Sorry you can't challenge yourself", ephemeral=True)
    else:  # Play against human
        print(f"{player1} is fighting {player2}")
        await interaction.response.send_message(f"{challenged.mention} you have been challenged\nchoose your weapon:", view=RPSbuttons(player1, player2, p1choice))



async def handle_winner(interaction ,Winner, p1choice, p2choice, player1, player2):
    if Winner == "null":
        await interaction.response.send_message(f"# It's a tie!\n*Both players chose `{p2choice}`*")
    elif Winner == player1:
        await interaction.response.send_message(f"# {player1.display_name} has won!\n*{player2.display_name} chose `{p2choice}`*\n*{player1.display_name} chose `{p1choice}`*")
    elif Winner == player2:
        await interaction.response.send_message(f"# {player2.display_name} has won!\n*{player1.display_name} chose `{p1choice}`*\n*{player2.display_name} chose `{p2choice}`*")


@bot.tree.command(name="vote", description="Adds a suggestion to the vote")
async def vote_command(interaction: discord.Interaction, suggestion: str):
    UserID = interaction.user.id
    ServerID = interaction.guild_id
    await dblogger.cmdcountup(UserID, ServerID)
    EventID = await dblogger.generate_event_id(8)
    Timestamp = datetime.now().strftime("%Y-%m-%d")
    await StoreVote(suggestion, UserID, ServerID, EventID, Timestamp)
    embed = discord.Embed(title="Suggestion Added", color=0x00ff00)
    embed.add_field(name="Suggestion", value=suggestion, inline=True)
    embed.add_field(name="EventID", value=EventID, inline=True)
    embed.set_footer(text="To remove this suggestion\nuse the EventID in the /vremove command")
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="vremove", description="use the Event ID of the vote to remove the vote from the list")
async def vremove_command(interaction: discord.Interaction, event_id: str):
    UserID = interaction.user.id
    ServerID = interaction.guild.id
    await dblogger.cmdcountup(UserID, ServerID)
    result = await RemoveVote(UserID, ServerID, event_id)
    if result == "invalid":
        await interaction.response.send_message(f"No suggestion found with the provided EventID.")
    if not result:
        await interaction.response.send_message(f"Successfully removed suggestion from list")

@bot.tree.command(name="vlist", description="show a list of suggestions made")
async def vlist_command(interaction: discord.Interaction):
    UserID = interaction.user.id
    ServerID = interaction.guild.id
    await dblogger.cmdcountup(UserID, ServerID)
    votes = await ViewVoteList(UserID, ServerID)
    embed = discord.Embed(title="List of Votes", color=0x00ff00)
    for vote in votes:
        embed.add_field(name=f"Suggestion: {vote[0]}", value=f"EventID: {vote[2]}\nBy: <@{vote[1]}>\nTimestamp: {vote[3]}", inline=False)
        embed.set_footer(text="To remove a suggestion\nuse the /vremove command with the designated EventID")
    if not votes:
        embed.add_field(name="Votes", value="No votes have been recorded.")
    # Send the embed as a response
    await interaction.response.send_message(embed=embed)



@bot.tree.command(name="vrun", description="Run the vote (randomised)")
async def RPScommand(interaction: discord.Interaction):
    UserID = interaction.user.id
    ServerID = interaction.guild.id
    await dblogger.cmdcountup(UserID, ServerID)
    # Fetch all votes from the database
    votes = await ViewVoteList(UserID, ServerID)


    # Check if there are any votes
    if not votes:
        await interaction.response.send_message("No suggestions found.")
        return

    # Randomly select a suggestion
    random_suggestion = random.choice(votes)

    # Create an embed with the randomly selected suggestion
    embed = discord.Embed(title="Randomly Selected Suggestion", color=0x00ff00)
    embed.add_field(name="Suggestion", value=random_suggestion[0], inline=False)
    embed.add_field(name="User ID", value=random_suggestion[1], inline=False)
    embed.add_field(name="Event ID", value=random_suggestion[2], inline=False)
    embed.add_field(name="Timestamp", value=random_suggestion[3], inline=False)

    # Send the embed to the user
    await interaction.response.send_message(embed=embed)
    print("running voteran")
    await Voteran(ServerID)
        
#run bot
# !! Change test_token to token BEFORE LAUNCH !!
bot.run(test_token)