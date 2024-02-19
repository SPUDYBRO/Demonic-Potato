import discord
import dblogger
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

description = '''Discord Bot :)'''

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

token, test_token = dblogger.tokengrabber()


@bot.command()
async def sync(ctx):
    try:
        synced = await bot.tree.sync()
        await ctx.send(f"Synced {len(synced)} commands")
        print("Bot Ready!")
    except Exception as e:
        await ctx.send(e)


@bot.command()
async def load(interaction, extension):
    await bot.load_extension(f"cogs.{extension}")

@bot.command()
async def unload(interaction, extension):
    await bot.unload_extension(f"cogs.{extension}")

@bot.command()
async def reload(interaction, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await bot.load_extension(f"cogs.{extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print (f"loaded Cog {filename[:-3]}")

bot.run(test_token)