#This file is used to hold all the constants for the game such as board size, piece colors, and values that dont change throughout the game.

BLACK = "X"
WHITE = "O"
BLANK = "-"
BOARDX = 8
BOARDY = 8
OFFSETS = [[1,1],[1,0],[1,-1],[0,1],[0,-1],[-1,1],[-1,0],[-1,-1]]
VALUEBOARD = [[10, 4, 4, 4, 4, 4, 4, 10], [4, 3, 2, 2, 2, 2, 3, 4], [4, 2, 1, 1, 1, 1, 2, 4], [4, 2, 1, 1, 1, 1, 2, 4], [4, 2, 1, 1, 1, 1, 2, 4], [4, 2, 1, 1, 1, 1, 2, 4], [4, 3, 2, 2, 2, 2, 3, 4], [10, 4, 4, 4, 4, 4, 4, 10]]
INFINITY = 999999999
winConditions = {"O":"White Wins","X":"Black Wins","-":"Tie"}
errorCodes = {0:"GENERALERROR"}
AINames = ["Rom","Belchi","Mahid","Mina","Aman","Ruben","Dyako","Eva","Magda","Rapunzel","Steve","Bob","Jeff","Geoff","Chris","Paige","Emily","Jenny","Tom","Will","Junior","Alex","Rose","Aleena","Zac","Nikki","Max","Anne","Jack","Sam","John","Tory","Tori","Imran","Punjabi MC","Jasmine","Rhianna","TJ","CJ","AJ","AI"]
tutorialText = ("""
Welcome to the game of othello.
In this game, your objective is to get more friendly pieces on the board than your opponent.
You may play against another player, or have an AI of one of four difficulties play against you.
Black (X) always moves first in this game.
Each turn, you get to place down one piece. 
The move is deemed valid if you can 'outflank' at least one enemy piece in a straight line.
This means it must be surrounded by 2 friendly pieces in a particular direction.
Pieces can be 'captured' if they are outflanked by the opposite piece, however it must be directly surrounded.
This means that only pieces that have been surrounded as a result of the newly placed piece can be captured.
There can be no cascade captures (Outflanked pieces that are surrounded but not by the piece last placed.)
If you do not have any valid moves to make, your turn is forfeited.
You cannot however, forfeit your turn if you have a valid move available.
Players are also not allowed to skip over their own color disks to outflank an opposing disk.
If you wish to learn more about the game, detailed instructions are available at-
https://www.worldothello.org/about/about-othello/othello-rules/official-rules/english
""")