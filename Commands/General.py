import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from discord.app_commands import Choice
import dblogger
from dblogger import *
import random


@app_commands.command(name="hello", description="Say hi to the bot")
async def hello_command(interaction: discord.Interaction):
    UserID = interaction.user.id
    ServerID = interaction.guild_id
    await dblogger.cmdcountup(UserID, ServerID,)
    greetings = ["Yo", "Sup", "Hello", "How you doin", "Nice to meet you!", "Greetings!", "Hi there!"]
    random_greeting = random.choice(greetings)
    await interaction.response.send_message(f"{random_greeting} {interaction.user.mention}", ephemeral=False)




async def setup(bot):
    bot.add_command(hello_command)