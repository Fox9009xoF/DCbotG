import discord
from discord.ext import commands
import json
import os

with open('C:\\Users\\10121\\Desktop\\DiscordBot\\GuraBot\\Gura_Bot\\setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("Gura is online")

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'other.{extension}')
    await ctx.send(f'Loaded {extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'other.{extension}')
    await ctx.send(f'UnLoaded {extension}')

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'other.{extension}')
    await ctx.send(f'ReLoaded {extension}')

for filename in os.listdir('./other'):
    if filename.endswith('.py'):
        bot.load_extension(f'other.{filename[:-3]}')

if __name__ == '__main__':
    bot.run(jdata['TOKEN'])