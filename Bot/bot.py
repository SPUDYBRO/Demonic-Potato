import discord
from discord.ext import commands
from Bot import dblogger
intents = discord.Intents()
intents.messages = True
intents.guilds = True
intents.members = True
intents.reactions = True
intents.typing = False
intents.message_content = True
intents.dm_messages = True
intents.webhooks = True
intents.bans = True
intents.presences = True
intents.guild_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


# Load commands
cogs_list = [
    'FunAndGames',
    'Basiccmd',
    'Messagecounters',
    'Moderation',

]
for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
        print("Bot Ready!")
    except Exception as e:
        print(e)


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
async def on_member_join(member):
    UserID = member.author.id
    ServerID = member.guild.id
    await dblogger.dbfixer(UserID, ServerID)