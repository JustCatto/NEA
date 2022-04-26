import AI
import human
import board
import constants
import replit
import pickle
import globalfunctions
import time
import os

class Game:
  def __init__(self):
    self.Version = 1.4

  def _loadDict(self,fileName): #Method to load and update the class dictionary to start the game again.
    f = open(fileName,"rb") #Opens the file as binary read only mode.
    temp = pickle.load(f) #Loads the dictionary and unpickles it.
    f.close() #Closes the file
    self.__dict__.update(temp) #Updates the dictionary with the data from the file.

  def _saveDict(self,fileName): #Method to save the class dictionary so the user can resume the game later.
    f = open(fileName,"wb") #Opens the file as binary write only mode.
    pickle.dump(self.__dict__,f,2) #Dumps the class dictionary in the file and pickles it.
    f.close() #Closes the file.

  def _checkIfFileExists(self,file): #Used before _saveDict to confirm the user wants to overwrite the existing file if it already exists.
    try: #Used to handle the error that is returned when opening a file as x (exclusive creation) if it already exists.
      f = open(file,"x") #Opens the file in mode x (exclusive creation)
      f.close()
    except FileExistsError:
      return True #If FileExistsError is returned, return true as the file exists.
    else:
      os.remove(file) #Since the file doesnt exist and was created, it must be removed to avoid any residual file.
      return False #If there is no error, return false as the file does not exist.

  def _getFileName(self,mode): #mode will be False if asking to load a file, or true if asking to save a file.
    while True:
      fileName = input("Please input the filename (Type exit to cancel)->")
      if fileName == "exit":
        return False
      if mode == False:
        if self._checkIfFileExists(fileName) == True:
          return fileName
        else:
          print("File does not exist")
      elif mode == True:
        if self._checkIfFileExists(fileName) == False:
          return fileName
        else:
          print("File already exists, would you like to overwrite the file?")
          while True:
            choice = input("Y/N\n-->").lower()
            if choice == "y":
              return fileName
            elif choice == "n":
              print("You have chosen not to overwrite the file.")
            else:
              print("Please input either y or n.")
        
  def _askForPlayerChoice(self,player): #Used to ask the user if the new player should be an AI or a human.
    print("Would you like player ",player,""" to be a player or a human?
          A for AI
          H for human""")
    while True:
      choice = input("--->").lower() #Gets the users input and makes it lowercase.
      if choice == "a": 
        return False #If the choice is a, return False to indicate the player wants an AI.
      elif choice == "h":
        return True #If the choice is h, return True to indicate the player wants a human (local player)
      else:
        print("Please enter either A or H.") #If the user doesnt input either a or h, tell the user to input either.

  def _askForAIDifficulty(self): #Asks the user what difficulty the AI should be 
    print("""What difficulty would you like the AI to be?
          E for easy
          M for medium
          H for hard
          VH for very hard""")
    while True: #Loops as long as there hasnt been a valid AI difficulty returned.
      choice = input("--->").lower() #takes the user input and makes it lowercase.
      if choice in ["e","m","h","vh"]: #If the user input is any valid difficulty, return it.
        return choice 
      else: #If the user input is not a valid difficulty, notify the user and ask them to type in the difficulty again.
        print("Invalid- Please enter one of the displayed options.")
    
  def _initialisePlayer1(self,humanPlayer): #Initialises the WHITE player/Player 1 class.
    if humanPlayer == True: #If humanplayer is true, ask for the players name and start an instance of the human class assigning it the WHITE piece.
      name = input("Please enter player 1's Name \n--->")
      self.player1 = human.Human(name,constants.WHITE)
    else: #Otherwise, start an instance of the AI class as the white piece and ask the user for its difficulty. The name is auto generated as the class initialises.
      self.player1 = AI.AI(constants.WHITE,self._askForAIDifficulty())
      
  def _initialisePlayer2(self,humanPlayer): #Does the same as _initialisePlayer1, however instead for player 2.
    if humanPlayer == True:
      name = input("Please enter player 2's Name \n--->")
      self.player2 = human.Human(name,constants.BLACK)
    else:
      self.player2 = AI.AI(constants.BLACK,self._askForAIDifficulty())

  def _saveGame(self,fileName): #Method that gets the user input for the name of the savefile.
    while True: #Only breaks the loop once the game class has been successfully saved.
      if self._checkIfFileExists(fileName) == True: #Checks if the file exists, if not just saves the file.
        overwrite = input("Would you like to overwite the file? [Y/N]").lower() #Changes the user input to lowercase and asks if they are sure.
        if overwrite == "y": #if y, overwrite the file.
          self._saveDict(fileName)
          break
        elif overwrite == "n": #If no, the loop is repeated again.
          pass
        else:
          print("Please enter either Y or N.") #If neither condition is met, notify the user that they must input either Y or N.
      elif self._checkIfFileExists(fileName) == False:
        self._saveDict(fileName)

  def _setNextMove(self,color): #Used if a move is undone or redone to override the next move.
    if color == constants.WHITE: #If the color input is white, set the turn to WHITE. (True)
      self.nextTurn = True
    elif color == constants.BLACK: #If the color input is black, set the turn to BLACK. (False)
      self.nextTurn = False
    else: #In the event that there is an incorrect variable input, return false to signify an error.
      globalfunctions.reportError(0)
      return False
      
  def _dealWithSpecialCondition(self,condition): #Method to deal with special conditions such as saving the game, undoing or redoing a move.
    if condition == "s":
      fileName = self._getFileName(True)
      if fileName != False:
        self._saveGame(fileName) #Calls the saveGame method to save the game dictionary before the game ends.
    elif condition == "r": #if the move is redone, the turn is not changed as it will still be the same players turn.
      self._setNextMove(self.othelloBoard.redoMove())
    elif condition == "u":
      status = self.othelloBoard.undoMove()
      if status == False: #If the move is undone, the turn does not change.
        print("No moves left to undo.")
    elif condition == "x":
      print("Game exiting.")
    else: #If none of the conditions are met, return an error to the user.
      globalfunctions.reportError(0)
      return False
        
  def _checkWinner(self): #Checks the winner by getting the total amount of WHITE and BLACK pieces.
    whitePieces = self.player1.getTotalPieces(self.othelloBoard.getBoard()) 
    blackPieces = self.player2.getTotalPieces(self.othelloBoard.getBoard())
    if whitePieces > blackPieces: #Whoever has the most pieces is declared the winner.
      print(constants.winConditions[constants.WHITE])
    elif whitePieces == blackPieces:
      print(constants.winConditions[constants.BLANK])
    elif whitePieces < blackPieces:
      print(constants.winConditions[constants.BLACK])
    pass

  def _playGame(self): #The method to play the game until it ends.
    outOfMoves = False #Initialises the variable to indicate if the enemy player does not have any moves.
    while True: #Loop that breaks when the game is over, or if the game is exited or saved.
      print(self.othelloBoard.getStackContents())
      if self.nextTurn == True: #If the turn is true, it is player 1's turn.
        move = self.player1.getMove(self.othelloBoard.getBoard()) #Gets the move for player 1.
        if move == False: #If the move from player 1 is false, this indicates there are no available moves for them.
          if outOfMoves == True: #If outOfMoves is true, this means that the enemy is also out of moves.
            print("Game Over, Both players have no valid moves remaining.")
            self._checkWinner() #This results in the games winner being checked and the loop being broken to end the game.
            break
          outOfMoves = True #If the enemy had moves last turn, indicate that one player is out of moves.
          self.nextTurn = False #Set the turn to the enemies turn.
        else:
          outOfMoves = False #If the user makes a move, set the condition to
          if move in ["s","u","r","x"]: #If the move is any of the special conditions, call the method to deal with it.
            self._dealWithSpecialCondition(move)
            if move in ["x","s"]: #if the move is to exit or save the game, break the while True loop to end the game.
              break
          else:
            self.othelloBoard.placePiece(move[0],move[1],move[2]) #If the move is not false or a special condition, attempt to place a piece on the board.
            self.nextTurn = False #Set the turn to BLACK.
      elif self.nextTurn == False: #If the turn is False, it is BLACK (player 2's) turn.
        move = self.player2.getMove(self.othelloBoard.getBoard()) #Same as above except for player 2.
        if move == False:
          if outOfMoves == True:
            print("Game over, both players have no valid moves remaining.")
            self._checkWinner()
            break
          outOfMoves = True
          self.nextTurn = True
        else:
          outOfMoves = False
          if move in ["s","u","r"]:
            self._dealWithSpecialCondition(move)
            if move in ["s","x"]:
              break
          else:
            self.othelloBoard.placePiece(move[0],move[1],move[2])
            self.nextTurn = True
          
  def _newGame(self): #Used to start the game using a blank board.
    self.nextTurn = True #True for whites move, false for blacks move. This is stored so that when the functions __dict__ is updated, it knows whos turn it should be next.
    self.othelloBoard = board.Board() #Initialises the board class and generates the board.
    self.othelloBoard.generateBoard()
    self._initialisePlayer1(self._askForPlayerChoice("1")) #Initialses both player 1 and 2.
    self._initialisePlayer2(self._askForPlayerChoice("2"))
    self._playGame() #Plays the game.

  def _loadGame(self,fileName):
    self._loadDict(fileName) #Updates the class dictionary.
    self._playGame() #Starts the game

  def mainMenu(self): #Prints the main menu for the user and hosts the game itself.
#    try:
      while True:
        print("Othello Game version-",self.Version)
        print("""
        ===MAIN MENU===
        1- New Game
        2- Load Game
        3- Exit Game
        """)
        while True:
          decision = input("Please enter your choice (1,2,3)\n--->") #Accepts the users input for what they want to do.
          if decision in ["1","2","3"]:
            break
          else:
            print("Invalid option, please try again.")
        if decision == "1": #If it is 1, starts a new game, if 2, loads a game from the existing file, and the 3rd stops the loop.
          replit.clear()
          self._newGame()
        elif decision == "2":
          replit.clear()
          fileName = self._getFileName(False)
          if fileName != False:
            self._loadGame(fileName)
        elif decision == "3":
          print("Exiting game")
          break
#    except Exception:
#      globalfunctions.reportError(0)