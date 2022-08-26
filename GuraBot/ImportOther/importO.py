import discord
from discord.ext import commands

class Cog_extention(commands.Cog):
    def __init__(self, bot):
        self.bot = bot