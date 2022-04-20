import player #Imports the player class to be inherited by the AI class.
import constants #Imports the constants class to be used for comparisons.
import random #Imports the random module to be used for picking a random name for the AI and for some of the AI difficulties.
import copy #Imports the copy module.
import time #Temporary module to slow down the AI moves
class AI(player.Player): #The player class inherits the player classes methods and atributes.

  def __init__(self,assignedPiece,AIDifficulty): #When the AI class is initialised, it needs the assigned piece (if it is player 1 or 2) and the difficulty.
    name = random.choice(constants.AINames) #the name of the AI is randomly picked when the class is initialised.
    super().__init__(name,assignedPiece) #Used to inherit the atributes for the player class.
    self.AIDifficulty = AIDifficulty #Sets the AI difficulty.

  def _simulatePlacePiece(self,othelloBoard,x,y,piece): #Method to be used to simulate a piece place that returns the state of the board after the piece is placed.
    offsets = constants.OFFSETS #Copies the offsets from the constants file to be used to check around the piece.
    othelloBoard[y][x] = piece #Sets the specified coordinates to be the specified piece.
    if piece == constants.WHITE: #Sets the oppositePiece variable to be the opposite piece of the original color piecce.
      oppositePiece = constants.BLACK
    elif piece == constants.BLACK:
      oppositePiece = constants.WHITE
    for offset in offsets: #Cycles through all the offsets of the board.
      flipPieces = [] #Clear/Initialise the flipPieces list.
      overallOffset = copy.copy(offset) #Makes a copy of the current offset.
      while True:
        checkY = y + overallOffset[1] #Create the coordinates to be searched in the board.
        checkX = x +overallOffset[0]
        if checkY not in range(0,constants.BOARDY) or checkX not in range(0,constants.BOARDX): #If the coordinates to be searched are out of the range of the board, break the loop early and search in another direction.
          break
        pieceToCheck = othelloBoard[checkY][checkX] #Get the piece in the space in the coordinates to be searched.
        if pieceToCheck == piece: #If the piece being checked is friendly, flip all the pieces in the flipPieces list to friendly.
          for flipPiece in flipPieces:
            othelloBoard[flipPiece[1]][flipPiece[0]] = piece
          break
        elif pieceToCheck == constants.BLANK: #if the piece is blank, clear the list and break the loop to search in another direction.
          flipPieces = []
          break
        elif pieceToCheck == oppositePiece: #If the piece is an enemy piece, add the coordinates of that piece to be flipped and add the original offset to the total offset to search the next piece in the same direction.
          flipPieces.append([checkX,checkY])
          overallOffset[1] += offset[1]
          overallOffset[0] += offset[0]
    return othelloBoard #Return the final state of the board after the piece is placed.

  def _calculateHeuristic(self,othelloBoard,mode): #Calculates roughly who is winning by reading the boards state. Positive means white is winning, negative means black is winning.
    score = 0 #Score always starts at 0. (Tie)
    if mode == False: #If the mode is set to false, do not use the spotValue 2D array and instead add/subtract one whenever either white or black piece is found.
      for x in range(constants.BOARDX):
        for y in range(constants.BOARDY):
          pieceScan = othelloBoard[y][x]
          if pieceScan == constants.WHITE:
            score += 1
          elif pieceScan == constants.BLACK:
            score -= 1
    elif mode == True: #If the mode is set to true, use the spotValue 2D array and add/subtract the value in the same coordinates as the found piece/
      for x in range(constants.BOARDX):
        for y in range(constants.BOARDY):
          pieceScan = othelloBoard[y][x]
          spotValue = constants.VALUEBOARD[y][x]
          if pieceScan == constants.WHITE:
            score += spotValue
          elif pieceScan == constants.BLACK:
            score -= spotValue
    print(score," Board Score")
    return score #At the end, once the heuristic of the board has been found, return it.

  def _minimax(self,othelloBoard,move,depth,maximising,alpha,beta,mode): #The minimax function that is used to calculate the best possible score the player can achieve in x moves (The depth)
    if maximising == True:
      color = self.assignedPiece
    else:
      color = self._swapColor(self.assignedPiece)
    newBoard = self._simulatePlacePiece(othelloBoard,move[0],move[1],color) #Simulates the piece being placed on a board.
    possibleMoves = self._getPossibleMoves(newBoard,maximising) #Gets the new possible moves after the piece has been simulated being placed on the board.
    if depth == 0 or possibleMoves == []: #If the depth is 0 or there are no possible moves remaining, calculate the heuristic of the board and stop searching downward.
      self._calculateHeuristic(newBoard,mode)
    if maximising == True: #If maximising is true, search for the highest heuristic possible out of all possible moves.
      maxHeuristic = -constants.INFINITY #Set the maximum to negative infinity so that no matter what, the first heuristic returned will always override this as it will always be higher.
      for possibleMove in possibleMoves: #Cycles through all possible moves.
        heuristic = self._minimax(self,newBoard,possibleMove,depth-1,False,alpha,beta) #Call the minimax function again with the possibleMove, passing through all other variables except lowering the depth by one and setting the maximising to False.
        if heuristic > maxHeuristic: #If the heuristic is higher than the maximum, replace the maxheuristic with the heuristic.
          maxHeuristic = copy.copy(heuristic) 
        if maxHeuristic <= beta: #If the beta at any point is lower than the maxHeuristic, stop searching through all the possible moves.
          break
        alpha = max(alpha,maxHeuristic) #Set the alpha to the max of itself and the maxHeuristic
      return maxHeuristic
    else: #Otherwise, if maximising is false, search for the lowest heuristic possible out of all possible moves.
      minHeuristic = +constants.INFINITY #Set the minimum to infinity so that no matter what, the first heuristic returned will always override this as it will always be lower.
      for possibleMove in possibleMoves: #Cycles through all possible moves.
        heuristic = self._minimax(self,newBoard,possibleMove,depth-1,True,alpha,beta) #Call the minimax function again with the possibleMove, passing through all other variables except lowering the depth by one and setting the maximising to True.
        if heuristic < minHeuristic: #if the heuristic found less than minHeuristic, replace it with the heuristic.
          minHeuristic = copy.copy(heuristic)
        if minHeuristic <= alpha: #If the alpha at any point is higher or equal to the minimum heuristic, stop searching through the possible moves.
          break
        beta = min(beta,minHeuristic) #Set the beta to be the minimum of either itself or the minimum heuristic.
      return minHeuristic #Once all moves have been searched return the minimum heuristic.

  def _minimaxInitialCall(self,board,possibleMoves,mode): #Used to initially call the minimax function with the first set of moves. 
    minHeuristic = -constants.INFINITY #Initialises the minHeuristic variable as -infinity so that the first heuristic that the board returns will always override the minimum.
    for possibleMove in possibleMoves: #Cycles through all the possible moves.
      heuristic = self._minimax(board,possibleMove,5,True,-constants.INFINITY,+constants.INFINITY,mode) #Initially calls the minimax method for each possible move.
      if heuristic > minHeuristic: #If the heuristic returned by the minimax function is higher than the minimum, set the minimum to the current moves heuristic, and the optimal move to the possibleMove.
        minHeuristic = copy.copy(heuristic)
        optimalMove = copy.copy(possibleMove)
    optimalMove.append(self.assignedPiece)
    return optimalMove #Once all possible moves have been checked, return the optimalMove.
    
  def _easyAIMove(self,possibleMoves): #Easy AI, picks a random move from the possibleMoves list.
    move = random.choice(possibleMoves)
    move.append(self.assignedPiece)
    return move

  def _mediumAIMove(self,othelloBoard,possibleMoves): #Medium AI, picks the move that returns the board with the highest heuristic
    maxMoveValue = -constants.INFINITY
    minMoveValue = +constants.INFINITY
    optimalMove = []
    for possibleMove in possibleMoves: #Cycles through all the possible moves.
      othelloBoardTest = copy.deepcopy(othelloBoard) #Makes a copy of the original board to be used for the _simulatePlacePiece method.
      othelloBoardTest = self._simulatePlacePiece(othelloBoardTest,possibleMove[0],possibleMove[1],self.assignedPiece) #Simulates the possibleMove and returns the board after the move was made.
      moveValue = self._calculateHeuristic(othelloBoardTest,False) #Returns the heuristic of the board after the move was made.
      if self.assignedPiece == constants.WHITE:
        if moveValue > maxMoveValue: #If the heuristic of the board is higher than the maximum heuristic encountered, replace the optimalMove with that move and the maxMoveValue with the moveValue.
          optimalMove = possibleMove
          maxMoveValue = moveValue
      elif self.assignedPiece == constants.BLACK:
        if moveValue < minMoveValue:
          optimalMove = possibleMove
          minMoveValue = moveValue
    optimalMove.append(self.assignedPiece)
    return optimalMove #Once all moves have been tried, return the optimal move.

  def _hardAIMove(self,othelloBoard,possibleMoves): #Minimax AI
    return self._minimaxInitialCall(othelloBoard,possibleMoves,False) #Calls the minimax function with the non-weighted board score heuristic.

  def _veryHardAIMove(self,othelloBoard,possibleMoves): #Minimax AI with improved piece values
    return self._minimaxInitialCall(othelloBoard,possibleMoves,True) #Calls the minimax function with the weighted board score heuristic.

  def getMove(self,othelloBoard): #Called by the game class to get the AIs move based on the difficulty.
    time.sleep(1)
    possibleMoves = []
    self._printBoard(othelloBoard)
    print("It is AI-",self.playerName,"'s turn.", self.AIDifficulty, "Diff")
    possibleMoves = self._getPossibleMoves(othelloBoard,True)
    if possibleMoves == []: #If there are no possible moves to take, return false. 
      print("No possible moves to take.")
      return False
    if self.AIDifficulty == "e": #Depending on the set AI difficulty, return the move that the methods return or return false if the AIDifficulty is in an invalid state.
      return self._easyAIMove(possibleMoves)
    elif self.AIDifficulty == "m":
      return self._mediumAIMove(othelloBoard,possibleMoves)
    elif self.AIDifficulty == "h":
      return self._hardAIMove(othelloBoard,possibleMoves)
    elif self.AIDifficulty == "vh":
      return self._veryHardAIMove(othelloBoard,possibleMoves)
    else:
      return False