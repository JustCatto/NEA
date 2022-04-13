from player import Player
import constants
import random
import copy

class AI(Player):

  def __init__(self,assignedPiece,AIDifficulty):
    name = random.choice(constants.AINames)
    super().__init__(name,assignedPiece)
    self.AIDifficulty = AIDifficulty

  def _simulatePlacePiece(self,othelloBoard,x,y,piece):
    flipPieces = []
    offsets = constants.OFFSETS
    othelloBoard[y][x] = piece
    if piece == constants.WHITE:
      oppositePiece = constants.BLACK
    elif piece == constants.BLACK:
      oppositePiece = constants.WHITE
    for offset in offsets:
      overallOffset = copy.copy(offset)
      while True:
        checkY = y + overallOffset[1]
        checkX = x +overallOffset[0]
        if checkY not in range(0,constants.BOARDY) or checkX not in range(0,constants.BOARDX):
          break
        pieceToCheck = othelloBoard[checkY][checkX]
        if pieceToCheck == piece:
          for flipPiece in flipPieces:
            self.othelloBoard[flipPiece[1]][flipPiece[0]] = piece
          break
        elif pieceToCheck == constants.BLANK:
          flipPieces = []
          break
        elif pieceToCheck == oppositePiece:
          flipPieces.append([checkX,checkY])
          overallOffset[1] += offset[1]
          overallOffset[0] += offset[0]
    return othelloBoard

  def _calculateHeuristic(self,othelloBoard,mode):
    score = 0
    if mode == False:
      for piece in othelloBoard:
        if piece == constants.WHITE:
          score += 1
        elif piece == constants.BLACK:
          score -= 1
    elif mode == True:
      for x in range(constants.BOARDX):
        for y in range(constants.BOARDY):
          pieceScan = othelloBoard[y][x]
          spotValue = constants.VALUEBOARD[y][x]
          if pieceScan == constants.WHITE:
            score += spotValue
          elif pieceScan == constants.BLACK:
            score -= spotValue
    return score

  def _minimax(self,othelloBoard,move,depth,maximising,alpha,beta,mode):
    newBoard = self._simulatePlacePiece(othelloBoard,move)
    possibleMoves = self._getPossibleMoves(newBoard)
    if depth == 0 or possibleMoves == []:
      self._calculateHeuristic(newBoard,mode)
    if maximising == True:
      maxHeuristic = -constants.infinity
      for possibleMove in possibleMoves:
        heuristic = self._minimax(self,newBoard,possibleMove,depth-1,False,alpha,beta)
        if heuristic > maxHeuristic:
          maxHeuristic = copy.copy(heuristic)
        if maxHeuristic <= beta:
          break
        alpha = max(alpha,maxHeuristic)
      return maxHeuristic
    else:
      minHeuristic = +constants.infinity
      for possibleMove in possibleMoves:
        heuristic = self._minimax(self,newBoard,possibleMove,depth-1,True,alpha,beta)
        if heuristic < minHeuristic:
          minHeuristic = copy.copy(heuristic)
        if minHeuristic <= alpha:
          break
        beta = min(beta,minHeuristic)
      return minHeuristic

  def _minimaxInitialCall(self,board,possibleMoves,mode):
    minHeuristic = -constants.INFINITY
    for possibleMove in possibleMoves:
      heuristic = self._minimax(board,possibleMove,5,True,-constants.INFINITY,+constants.INFINITY,mode)
      if heuristic > minHeuristic:
        minHeuristic = copy.copy(heuristic)
        optimalMove = copy.copy(possibleMove)
    return optimalMove


    
  def _easyAIMove(self,possibleMoves): #Dumdum AI
    move = random.choice(possibleMoves)
    move.append(self.assignedPiece)
    return move

  def _mediumAIMove(self,othelloBoard,possibleMoves): #Slightly OK AI
    maxMoveValue = -999999999
    optimalMove = []
    for possibleMove in possibleMoves:
      othelloBoardTest = copy.deepcopy(othelloBoard)
      othelloBoardTest = self._simulatePlacePiece(othelloBoardTest,possibleMove[0],possibleMove[1],self.assignedPiece)
      moveValue = self._calculateHeuristic(othelloBoardTest,True)
      if moveValue > maxMoveValue:
        optimalMove = possibleMove
        maxMoveValue = moveValue
    return optimalMove

  def _hardAIMove(self,othelloBoard,possibleMoves): #Minimax AI
    return self.minimaxInitialCall(othelloBoard,possibleMoves,False)

  def _veryHardAIMove(self,othelloBoard,possibleMoves): #Minimax AI with improved piece values
    return self.minimaxInitialCall(othelloBoard,possibleMoves,True)

  def getMove(self,othelloBoard):
    possibleMoves = []
    print("It is AI-",self.playerName,"'s turn.")
    possibleMoves = self._getPossibleMoves(othelloBoard,True)
    if possibleMoves == []:
      print("No possible moves to take.")
      return False
    if self.AIDifficulty == "e":
      return self._easyAIMove(possibleMoves)
    elif self.AIDifficulty == "m":
      return self._mediumAIMove(othelloBoard,possibleMoves)
    elif self.AIDifficulty == "h":
      return self._hardAIMove(othelloBoard,possibleMoves)
    elif self.AIDifficulty == "vh":
      return self._veryHardAIMove(othelloBoard,possibleMoves)
    else:
      return False