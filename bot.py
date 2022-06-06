from discord.ext import commands
from discord import *
import asyncio
import os

bot = commands.Bot('&', description="Illuminum666\'s bot")

@bot.event
async def on_ready():
    await bot.change_presence(status=Status.online, activity=Game("Among Us"))
    print("Bot is online")

@bot.command()
@commands.is_owner()
async def stop(ctx):
    await bot.change_presence(status=Status.offline)
    await bot.logout()
    await bot.close()

for f in os.listdir("./cogs"):
    if f.endswith(".py") and not f in ("tests.py", "__init__.py"):
        bot.load_extension(f"cogs.{f[:-3]}")
        print(f"Loaded cog: {f}")

# un-comment for testing
# bot.load_extension("cogs.tests")
    
with open('./login.txt') as f:
    TOKEN = f.read().strip()

bot.run(TOKEN)