# libraries
from math import floor
from random import randint, sample
from emoji import emojize

from discord.ext import commands
from discord import *

emojieqv = {
    1: ":one:",
    2: ":two:",
    3: ":three:",
    4: ":four:",
    5: ":five:",
    6: ":six:",
    7: ":seven:",
    8: ":eight:",
    9: ":nine:",
    0: ":zero:",
    "a": ":regional_indicator_a:",
    "b": ":regional_indicator_b:",
    "c": ":regional_indicator_c:",
    "d": ":regional_indicator_d:",
    "e": ":regional_indicator_e:",
    "f": ":regional_indicator_f:",
    "g": ":regional_indicator_g:",
    "h": ":regional_indicator_h:",
    "i": ":regional_indicator_i:"
}

class cell:
    def __init__(self) -> None:
        self.disp = 0
        self.sol = 0
        self.possibleValues = set()


class board:
    def __init__(self, ctx) -> None:
        self.ctx = ctx
        self.space = [[cell() for _ in range(9)] for _ in range(9)]

    # prints out playing board
    async def print(self, title: str) -> None:
        name = ""
        value = ""
        boardemb = Embed(
            title = title
        )

        # initial header
        name += ":blue_square:"
        for i in range(9):
            name += emojize(emojieqv[chr(i + 97)])
            if i % 3 == 2: name += "᲼᲼᲼"

        # board part
        # doing it all in one string apparently exceeds the character limit, so three separate fields are used
        for i in range(9):
            value += emojize(emojieqv[chr(i + 97)])
            for j in range(9):
                value += emojize(emojieqv[self.space[i][j].disp] if not self.space[i][j].disp == 0 else ":black_large_square:")
                if j % 3 == 2 and not j == 8: value += "᲼᲼᲼"
            value += "\n"
            if i % 3 == 2:
                boardemb.add_field(name=name, value=value, inline=False)
                name = "\u200b"
                value = ""
        
        # part that shows missing numbers
        value = ""
        for i in self.toFill:
            if not self.toFill[i] == 0: value += f"{emojieqv[i]}: {self.toFill[i]}᲼᲼"
        boardemb.add_field(name="Remaining Numbers to Fill:", value=value, inline=False)

        # part that shows instructions
        boardemb.add_field(name="Instructions:", value="Reply with the number to enter and location to enter\ne.g. 6ab: enter number 6 at cell located at row a and column b (lowercase)", inline=False)
        
        # sends out the full thing
        await self.ctx.send(embed=boardemb)

    # prints out solution
    async def printSol(self) -> None:
        name = ""
        value = ""
        boardemb = Embed(
            title = "Solution"
        )

        # initial header
        name += ":blue_square:"
        for i in range(9):
            name += emojize(emojieqv[chr(i + 97)])
            if i % 3 == 2: name += "᲼᲼᲼"

        # board part
        # doing it all in one string apparently exceeds the character limit, so three separate fields are used
        for i in range(9):
            value += emojize(emojieqv[chr(i + 97)])
            for j in range(9):
                value += emojize(emojieqv[self.space[i][j].sol])
                if j % 3 == 2 and not j == 8: value += "᲼᲼᲼"
            value += "\n"
            if i % 3 == 2:
                boardemb.add_field(name=name, value=value, inline=False)
                name = "\u200b"
                value = ""

        # sends out the full thing
        await self.ctx.send(embed=boardemb)
    
    # to use during solution board
    # if val is unique in row, col and subsq, add into possible values
    def addUnique(self, row, col, val) -> None:
        for i in range(3):
            for j in range(3):
                if self.space[i * 3 + j][col].sol == val or self.space[row][i * 3 + j].sol == val or self.space[floor(row / 3) * 3 + i][floor(col / 3) * 3 + j].sol == val:
                    return
        self.space[row][col].possibleValues.add(val)

    # create solution board
    def generateSol(self) -> None:
        row, col = 0, 0
        while not (row == 9 and col == 0):
            # reset possible values for given cell
            self.space[row][col].possibleValues.clear()
            for num in range(1, 10):
                self.addUnique(row, col, num)
            
            # backtrack till there are possible values
            while len(self.space[row][col].possibleValues) == 0:
                col -= 1
                if col == -1:
                    col = 8
                    row -= 1
                self.space[row][col].possibleValues.remove(self.space[row][col].sol)
                self.space[row][col].sol = 0
            
            # input random number into solution board from set of possible values
            self.space[row][col].sol = sample(list(self.space[row][col].possibleValues), 1)[0]
            
            # move to next cell
            col += 1
            if col == 9:
                col = 0
                row += 1
    
    # create challenge board
    # returns dict of num of each color to fill into board
    def createChallenge(self, removeN):
        self.toFill = dict((i + 1, 0) for i in range(9))

        # copies sol board to challenge board
        for i in range(9):
            for j in range(9):
                self.space[i][j].disp = self.space[i][j].sol
        
        # remove N
        for i in range(removeN):
            while True:
                row, col = randint(0, 8), randint(0, 8)
                if not self.space[row][col].disp == 0:
                    break
            self.toFill[self.space[row][col].disp] += 1
            self.space[row][col].disp = 0

    # to use during play state
    # returns bool based on whether space is filled or not
    def filledSpace(self, row, col) -> bool:
        if self.space[row][col].disp == 0:
            return False
        return True