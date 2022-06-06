from discord.ext import commands
from discord import *

class General(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def echo(self, ctx, *, text):
        await ctx.send(text)

    @commands.command()
    async def mogus(self, ctx):
        await ctx.send("SUS! " * 100)

def setup(client):
    client.add_cog(General(client))