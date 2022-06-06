from .Sudoku.boardObjects import board
from .Sudoku.engine import gameEngine
from discord.ext import commands
from discord import *

class Game(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def sudoku(self, ctx):
        player = ctx.message.author
        print(f"\n{player} is now playing Sudoku\n")
        game = gameEngine(ctx, player)
        await game.runGame(self.client)
        print(f"\n{player} has finished playing Sudoku\n")

def setup(client):
    client.add_cog(Game(client))
