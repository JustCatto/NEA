from player import Player
import replit
import time

class Human(Player):
  
  def __init__(self,playerName,assignedPiece):
    super().__init__(playerName,assignedPiece)

  def _printPossibleMoves(self,moveList):
    print("POSSIBLE MOVES-\n")
    for move in moveList:
      x = str(move[0] + 1)
      y = str(move[1] + 1)
      print("[",x,",",y,"]", end = ", ")
    print("\n")

  def _printBoard(self,othelloBoard):
    print(" ", end = " ")
    for x in range(8): 
      print(x + 1, end = " ")
    print(" ") 
    for y in range(8):
      print(y + 1, end = " ") 
      for x in range(8):
        print(othelloBoard[y][x],end = " ") 
      print(" ")

  def _confirmDecision(self):
    while True:
      choice = input("Are you sure? (Y/N)").lower()
      if choice == "y":
        return True
      elif choice == "n":
        return False
      else:
        print("Invalid input, please try again")
        time.sleep(2)
        replit.clear()
    
  def _getCoordinates(self,othelloBoard,possibleMoves):
    while True:
      replit.clear()
      self._printBoard(othelloBoard)
      self._printPossibleMoves(possibleMoves)
      try:
        x = int(input("Please enter the x coordinates (Top bar) for the space.")) - 1
        y = int(input("Please enter the y coordinates (side bar) for the space.")) - 1
        if [x,y] in possibleMoves and x in range(0,constants.BOARDX) and y in range(0,constants.BOARDY):
          return [x,y,self.assignedPiece]
        else:
          print("Please enter a possible move.")
          time.sleep(1.5)
      except ValueError:
        print("Please enter a number.")
        time.sleep(1.5)
        
  
  def getMove(self,othelloBoard):
    possibleMoves = self._getPossibleMoves(othelloBoard,True)
    while True:
      print("It is",self.playerName,"'s turn.'")
      self._printBoard(othelloBoard)
      self._printPossibleMoves(possibleMoves)
      Choice = input("""M to input coordinates for a move
                     U to undo the last move
                     R to redo the last undo
                     S to save the game
                     X to exit the game without saving""").lower()
      if Choice == "u":
        print("You have chosen to undo your last move.")
        if self._confirmDecision() == True:
          return Choice
      elif Choice == "r":
        print("You have chosen to redo your last undo.")
        if self._confirmDecision() == True:
          return Choice
      elif Choice == "s":
        print("You have chosen to save the game.")
        if self._confirmDecision() == True:
          return Choice
      elif Choice == "x":
        print("You have chosen to exit the game without saving.")
        if self._confirmDecision() == True:
          return Choice
      elif Choice == "m":
        print("You have chosen to take a move.")
        if self._confirmDecision() == True:
          return self._getCoordinates(othelloBoard,possibleMoves)
          
      
        