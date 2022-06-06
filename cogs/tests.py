from discord.ext import commands
from discord import *

class Testing(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command()
    async def checkCache(self, ctx):
        await ctx.send(self.client.cached_messages)
    @commands.command()
    async def waitfortest(self, ctx):
        await ctx.send("react")
        await self.client.wait_for("reaction_add")
        await ctx.send("hi")
    @commands.command()
    async def authortest(self, ctx):
        user = ctx.message.author
        await ctx.send(user)
        await ctx.send(user.name)

def setup(client):
    client.add_cog(Testing(client))