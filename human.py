import player #Imports the player class to be inherited by the Human class.
import replit  #Imports replit to be used to clear the console to provide a clutter free console.
import time #Used for delays in displaying text.
import constants #Used to get constants such as board dimentions 
import globalfunctions #Imports all of the functions that are used in all class files.

class Human(player.Player): #This class is used to represent a human player.
  
  def __init__(self,playerName,assignedPiece): #Has two arguments, the players name and the assigned piece for the class.
    super().__init__(playerName,assignedPiece) #Initialises the inherited values from the player class.

  def _printPossibleMoves(self,moveList): #Used to print off the possible moves for the user.
    print("POSSIBLE MOVES-\n")
    for move in moveList: #Cycles through all the moves in the possible move list.
      x = str(move[0] + 1) #Gives an offset of +1 to both the x and y coordinates for the move.
      y = str(move[1] + 1) #This is because of the indicators starting at 1, and the actual reference for the coordinates starting at 0.
      print("[",x,",",y,"]", end = ", ") #Prints off one of the coordinates, end = "," is to override the default so it prints on the same line.
    print("\n") #Prints a new line one all coordinates are printed.

  def _confirmDecision(self): #Used to confirm the users decision. Called whenever a user is asked for an input.
    while True: #Runs the loop 
      choice = input("Are you sure? (Y/N)").lower() #Asks for user input if they are sure.
      if choice == "y":
        return True #Breaks the loop and returns true, indicating the user is sure of their chocie.
      elif choice == "n":
        return False #Breaks the loop and returns false, indicating the user wants to change their choice.
      else:
        print("Invalid input, please try again") #If the user does not type either Y or N, print this and clear the last confirmation text.
        time.sleep(2)
        replit.clear() 
    
  def _getCoordinates(self,othelloBoard,possibleMoves): #Method to recieve user input for the coordinates for the piece.
    if possibleMoves == []: #If there are no possible moves, return false so that the game class knows.
      print("No possible moves for player-",self.playerName,"'s turn.")
      return False
    while True:
      replit.clear()
      self._printBoard(othelloBoard)
      self._printPossibleMoves(possibleMoves)
      try:
        x = int(input("Please enter the x coordinates (Top bar) for the space.")) - 1 #Asks the user to input the coordinates for the space they want to place down.
        y = int(input("Please enter the y coordinates (side bar) for the space.")) - 1
      except ValueError: #If either X or Y is not an number, return an error and ask the user to input the coordinates again.
        print("Please enter a number.")
        time.sleep(1.5)
      else:
        if [x,y] in possibleMoves and x in range(0,constants.BOARDX) and y in range(0,constants.BOARDY): #If the coordinates are in the possible move list,
          return [x,y,self.assignedPiece]                                                                #And in the range of the board constants, return the coordinates.
        else: 
          print("Please enter a possible move.") #If it is not a possible move, print to the user that it isnt possible and ask them to input the coordinates again.
          time.sleep(1.5)
        
  def getMove(self,othelloBoard): 
    possibleMoves = self._getPossibleMoves(othelloBoard,True) #Gets the possible moves for the current board state.
    while True: #If there are possible moves, ask for the users input.
      print("It is",self.playerName,"'s turn.'")
      self._printBoard(othelloBoard) #Prints out the board and the possible coordinates for the user.
      self._printPossibleMoves(possibleMoves) 
      Choice = input("""
                     M to input coordinates for a move
                     U to undo the last move
                     R to redo the last undo
                     S to save the game
                     X to exit the game without saving""").lower() #Prints out the users options, and takes their input and puts it into lower case.
      if Choice == "u": #If the user inputs any of the below letters (y,r,s,x,m), the user is asked if they are sure and if so, the contents of choice are returned for the game class to handle.
        print("You have chosen to undo your last move.") #The only exception to the above line is for m, where the coordinates are returned instead.
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
        if possibleMoves == []:
          print("Warining- You do not have any possible moves. By confirming, you will have your turn skipped.")
        if self._confirmDecision() == True:
          return self._getCoordinates(othelloBoard,possibleMoves) #Calls the private method to get the user coordinates using the board and possible moves.
          
      
        