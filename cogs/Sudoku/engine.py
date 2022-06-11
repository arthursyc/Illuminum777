# libraries
from time import time
from re import match
from asyncio import TimeoutError

from discord.ext import commands
from discord import *

# local modules
from .boardObjects import board


class gameEngine:
    def __init__(self, ctx, player) -> None:
        self.ctx = ctx
        self.board = board(self.ctx)
        self.player = player
        self.lives = 3
        self.stopGame = False

    # asks player for game difficulty
    # returns int for number of cells to clear for challenge
    async def getDifficulty(self, client: commands.Bot) -> int:
        diffmsg = await self.ctx.send(embed=Embed(title="Difficulty?"))
        await diffmsg.add_reaction("\U0001F1EA")
        await diffmsg.add_reaction("\U0001F1F2")
        await diffmsg.add_reaction("\U0001F1ED")

        def check(reaction, user):
            return reaction.emoji in ["\U0001F1EA", "\U0001F1F2", "\U0001F1ED"] and user == self.player and reaction.message == diffmsg
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=6000.0, check=check)
        except TimeoutError:
            await self.ctx.send(embed=Embed(title=f"Game by {self.player} not started"))
            self.stopGame = True
            return None

        match reaction.emoji:
            case "\U0001F1EA":
                return 30
            case "\U0001F1F2":
                return 40
            case "\U0001F1ED":
                return 50

    # asks player for what and where to enter during play state
    # input validation included except checking whether cell to enter is filled or not
    async def getInput(self, client: commands.Bot):
        # get input val
        def check(msg):
            return bool(match("[1-9][a-i][a-i]", msg.content)) and msg.author == self.player
        try:
            msg = await client.wait_for("message", timeout=6000.0, check=check)
        except TimeoutError:
            await self.ctx.send(embed=Embed(title=f"Game by {self.player} has timed out"))
            self.stopGame = True
            return
        self.val, self.row, self.col = msg.content
    
        # converts value into int and row and col into indices
        self.val = int(self.val)
        self.row, self.col = ord(self.row) - 97, ord(self.col) - 97

    # plays the game
    async def runGame(self, client) -> None:
        self.numToSolve = await self.getDifficulty(client)
        if self.stopGame: return None
        
        self.board.generateSol()
        self.board.createChallenge(self.numToSolve)
        title=f"Starting lives: {self.lives}"
        self.starttime = time()

        # game loop, ends when cells are filled or lives are out
        while self.numToSolve > 0 and not self.lives == 0:
            await self.board.print(title=title)

            # gets and valids player input for what and where to enter
            while True:
                await self.getInput(client)
                if self.stopGame: return None
                if not self.board.filledSpace(self.row, self.col):
                    break
                await self.board.print(title=f"Player: {self.player}\nCan't place there!")

            # determines whether input is correct or not, fills cell if correct, reduce lives if not
            if not self.board.space[self.row][self.col].sol == self.val:
                self.lives -= 1
                title = f"Player: {self.player}\nThat's not right! Remaining lives: {self.lives}"
            else:
                self.board.space[self.row][self.col].disp = self.val
                self.numToSolve -= 1
                self.board.toFill[self.val] -= 1
                title = f"Player: {self.player}\nThat's right! Remaining lives: {self.lives}"


        # get total time spent, capped at 99:59
        self.timeSpent = int(time() - self.starttime)
        if self.timeSpent > 5999: self.timeSpent = 5999

        # announce game results
        if not self.lives == 0:
            await self.ctx.send(embed=Embed(title=f"Game finished, {self.player} has won!", description=f"Remaining lives: {self.lives}\nTime spent: {str(self.timeSpent // 60).zfill(2)}:{str(self.timeSpent % 60).zfill(2)}"))
        else:
            await self.ctx.send(embed=Embed(title=f"Game over, {self.player} has lost.", description=f"Time spent: {str(self.timeSpent // 60).zfill(2)}:{str(self.timeSpent % 60).zfill(2)}"))
            await self.board.printSol()