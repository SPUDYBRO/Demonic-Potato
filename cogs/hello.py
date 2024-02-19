import discord
import dblogger
import random
from discord.ext import commands


class Hello(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.tree.command(name="hello", description="Say hi to the bot")
    async def hello_command(self, interaction: discord.Interaction):
        
        UserID = interaction.user.id
        ServerID = interaction.guild_id
        await dblogger.cmdcountup(UserID, ServerID,)
        greetings = ["Yo", "Sup", "Hello", "How you doin", "Nice to meet you!", "Greetings!", "Hi there!"]
        random_greeting = random.choice(greetings)
        await interaction.response.send_message(f"{random_greeting} {interaction.user.mention}", ephemeral=False)


def setup(bot):
    bot.add_cog(Hello(bot))