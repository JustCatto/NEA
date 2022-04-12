import AI
import human
import board
import constants
import replit
import pickle

class Game:
  def __init__(self):
    self.Version = 1.4
    self.nextTurn = True #True for whites move, false for blacks move. This is stored so that when the functions __dict__ is updated, it knows whos turn it should be next.
  def _loadDict(self,fileName):
    f = open(fileName,"rb")
    temp = pickle.load(f)
    f.close()
    self.__dict__.update(temp)

  def _saveDict(self,fileName):
    f = open(fileName,"wb")
    pickle.dump(__dict__,f,2)
    f.close()
  def _checkIfFileExists(self,file):
    try:
      f = open(file,"x")
      return False
    except FileExistsError:
      return True
    
  def _askForPlayerChoice(self,player):
    print("Would you like player ",player,""" to be a player or a human?
          A for AI
          H for human""")
    while True:
      choice = input("--->").lower()
      if choice == "a":
        return False
      elif choice == "h":
        return True
      else:
        print("Please enter either A or H.")

  def _askForAIDifficulty(self):
    print("""What difficulty would you like the AI to be?
          E for easy
          M for medium
          H for hard
          VH for very hard""")
    while True:
      choice = input("--->").lower()
      if choice in ["e","m","h","vh"]:
        return choice
      else:
        print("Invalid- Please enter one of the displayed options.")
    
  def _initialisePlayer1(self,humanPlayer):
    if humanPlayer == True:
      name = input("Please enter player 1's Name \n--->")
      self.player1 = human.Human(name,constants.WHITE)
    else:
      self.player1 = AI.AI(constants.WHITE,self._askForAIDifficulty())
      

  def _initialisePlayer2(self,humanPlayer):
    if humanPlayer == True:
      name = input("Please enter player 2's Name \n--->")
      self.player2 = human.Human(name,constants.BLACK)
    else:
      self.player2 = AI.AI(constants.BLACK,self._askForAIDifficulty())

  def _saveGame(self):
    while True:
      fileName = input("Please enter a name for your save file.")
      if self._checkIfFileExists(fileName) == True:
        overwrite = input("Would you like to overwite the file? [Y/N]").lower()
        if overwrite == "y":
          self._saveDict(fileName)
          break
        elif overwrite == "n":
          pass
        else:
          print("Please enter either Y or N.")

  def _setNextMove(self,color):
    if color == constants.WHITE:
      self.nextTurn = True
    elif color == constants.BLACK:
      self.nextTurn = False
    else:
      return False
      
  def _dealWithSpecialCondition(self,condition):
    if condition == "s":
      self._saveGame()
    elif condition == "r":
      status = board.redoMove()
      if status != False:
        self._setNextMove(status)
      else:
        pass  
    elif condition == "u":
      status = board.undoMove()
      if status != False:
        self._setNextMove(status)
      else:
        pass
    
      
      
  def _playGame(self):
    while True:
      if self.nextTurn == True:
        move = self.player1.getMove(self.othelloBoard.getBoard())
        if move in ["s","u","r"]:
          self._dealWithSpecialCondition(move)
        if move in ["x","s"]:
          break
        else:
          self.othelloBoard.placePiece(move[0],move[1],move[2])
          self.nextTurn = False
      elif self.nextTurn == False:
        move = self.player2.getMove(self.othelloBoard.getBoard())
        if move in ["s","u","r"]:
          self._dealWithSpecialCondition(move)
        if move in ["s","x"]:
          break
        else:
          self.othelloBoard.placePiece(move[0],move[1],move[2])
          self.nextTurn = True
          
  def _newGame(self):
    self.othelloBoard = board.Board()
    self.othelloBoard.generateBoard()
    self._initialisePlayer1(self._askForPlayerChoice("1"))
    self._initialisePlayer2(self._askForPlayerChoice("2"))
    self._playGame()
    
  def _loadGame(self,fileName):
    self._loadDict(fileName)
    self._playGame()
  def mainMenu(self):
    while True:
      print("Othello Game version-",self.Version)
      print("""
      ===MAIN MENU===
      1- New Game
      2- Load Game
      3- Exit Game
      """)
      while True:
        decision = input("Please enter your choice (1,2,3)\n--->")
        if decision in ["1","2","3"]:
          break
        else:
          print("Invalid option, please try again.")
      if decision == "1":
        replit.clear()
        self._newGame()
      elif decision == "2":
        replit.clear()
        self._loadGame()
      elif decision == "3":
        print("Exiting game")
        break