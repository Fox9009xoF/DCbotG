import discord
from discord.ext import commands
from ImportOther.importO import Cog_extention
import json
import random

with open('C:\\Users\\10121\\Desktop\\DiscordBot\\GuraBot\\Gura_Bot\\setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class voice(Cog_extention):

    @commands.command()
    async def voicejoin(self, ctx):
        if ctx.author.voice:
            channel = ctx.message.author.voice.channel
            if ctx.voice_client:
                await ctx.send("已經在語音頻道了")
            else:
                await channel.connect()
        else:
            await ctx.send("先進去語音頻道")
    
    @commands.command()
    async def voiceleave(self, ctx):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send("你想趕我走?!!!")


def setup(bot):
    bot.add_cog(voice(bot))