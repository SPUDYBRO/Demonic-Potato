import discord
from discord.ext import commands

class Listeners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print ("the bot is ready yippy")

def setup(bot):
    bot.add_cog(Listeners(bot))