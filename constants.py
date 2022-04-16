#This file is used to hold all the constants for the game such as board size, piece colors, and values that dont change throughout the game.

BLACK = "X"
WHITE = "O"
BLANK = "-"
BOARDX = 8
BOARDY = 8
OFFSETS = [[1,1],[1,0],[1,-1],[0,1],[0,-1],[-1,1],[-1,0],[-1,-1]]
VALUEBOARD = [['25', '10', '10', '10', '10', '10', '10', '25'], ['10', '7', '5', '5', '5', '5', '7', '10'], ['10', '5', '3', '2', '2', '3', '5', '10'], ['10', '5', '2', '1', '1', '2', '5', '10'], ['10', '5', '2', '1', '1', '2', '5', '10'], ['10', '5', '3', '2', '2', '3', '5', '10'], ['10', '7', '5', '5', '5', '5', '7', '10'], ['25', '10', '10', '10', '10', '10', '10', '25']]
INFINITY = 999999999
winConditions = {"O":"White Wins","X":"Black Wins","-":"Tie"}
errorCodes = {0:"GENERALERROR"}
AINames = ["Rom","Belchi","Mahid","Mina","Aman","Ruben","dyako","Eva","Magda","Rapunzel","Steve","Bob","Jeff","Geoff","Chris","Paige","Emily","Jenny","Tom","Will","Junior","Alex","Rose","Aleena","Zac","Nikki","Max","Anne","Jack","Sam","John","Tory","Tori","Imran","Punjabi MC","Jasmine","Rhianna","TJ","CJ","AJ","AI"]