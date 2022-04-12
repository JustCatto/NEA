import constants
import copy
class Player:

  def __init__(self,playerName,assignedPiece):
    self.playerName = playerName
    self.assignedPiece = assignedPiece
    self.totalPieces = []

  def _findPiece(self,othelloBoard,piece):
    coordinateList = []
    for x in range(constants.BOARDX):
      for y in range(constants.BOARDY):
        if othelloBoard[y][x] == piece:
          coordinateList.append([x,y])
    return coordinateList

  def _swapColor(self,color):
    if color == constants.BLACK:
      return constants.WHITE
    elif color == constants.WHITE:
      return constants.BLACK
    else:
      reportError(0)

  def _getPossibleMoves(self,othelloBoard,Friendly):
    if Friendly == True:
      piece = self.assignedPiece
      oppositePiece = self._swapColor(self.assignedPiece)
    else:
      piece = _swapColor(self.assignedPiece)
      oppositePiece = self.assignedPiece
    offsets = constants.OFFSETS
    possibleMoves = []
    pieceCoordinates = self._findPiece(othelloBoard,piece)
    for coordinate in pieceCoordinates:
      for offset in offsets:
        oppositePiecesInPath = 0
        overallOffset = copy.copy(offset)
        while True:
          checkX = coordinate[0] + overallOffset[0]
          checkY = coordinate[1] + overallOffset[1]
          if checkX not in range(0,8) or checkY not in range(0,8):
            break
          pieceToCheck = othelloBoard[checkY][checkX]
          if pieceToCheck == constants.BLANK:
            if oppositePiecesInPath != 0 and [checkX,checkY] not in possibleMoves:
              possibleMoves.append([checkX,checkY])
            break
          elif pieceToCheck == oppositePiece:
            oppositePiecesInPath += 1
            overallOffset[0] += offset[0]
            overallOffset[1] += offset[1] 
          elif pieceToCheck == piece:
            break
          else:
            break
    return possibleMoves
        