import discord
from discord.ext import commands
from ImportOther.importO import Cog_extention
import json

with open('C:\\Users\\10121\\Desktop\\DiscordBot\\GuraBot\\Gura_Bot\\setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class detector(Cog_extention):

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "!your mother":
            await message.channel.send("操你媽")

def setup(bot):
    bot.add_cog(detector(bot))