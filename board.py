import constants 
import copy
import stack
import globalfunctions
class Board:
  def __init__(self):
    self.othelloBoard = []
    self.pieceCoordinates = []
    self.nextMove = constants.BLANK
    self.undoRedoMoves = stack.Stack()

  def _swapColor(self,color):
    if color == constants.BLACK:
      return constants.WHITE
    elif color == constants.WHITE:
      return constants.BLACK
    else:
      globalfunctions.reportError(0)

  def generateBoard(self): 
    self.othelloBoard = [[constants.BLANK for x in range(8)]for y in range(8)] 
    self.piece = constants.BLACK
    for x in range(2):
      self.piece = self._swapColor(self.piece) 
      for y in range(2):
        self.othelloBoard[y+3][x+3] = self.piece 
        self.piece = self._swapColor(self.piece) 
    self.nextMove = constants.WHITE

  def placePiece(self,x,y,piece):
    flipPieces = []
    offsets = constants.OFFSETS
    self.othelloBoard[y][x] = piece
    oppositePiece = self._swapColor(piece)
    self.undoRedoMoves.pushCoordinates(x,y,piece)
    for offset in offsets:
      overallOffset = copy.copy(offset)
      while True:
        checkY = y + overallOffset[1]
        checkX = x +overallOffset[0]
        if checkY not in range(0,constants.BOARDY) or checkX not in range(0,constants.BOARDX):
          break
        pieceToCheck = self.othelloBoard[checkY][checkX]
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

  def undoMove(self):
    flipPieces = []
    Coordinate = self.undoRedoMoves.getUndoCoordinate()
    if Coordinate == False:
      print("Unable to undo move, no moves left to undo.")
      return False
    offsets = constants.OFFSETS
    pieceX = Coordinate[0]
    pieceY = Coordinate[1]
    pieceColor = Coordinate[2]
    oppositePieceColor = self._swapColor(pieceColor)
    self.othelloBoard[pieceY][pieceX] = constants.BLANK
    for offset in offsets:
      overallOffset = copy.copy(offset)
      while True:
        checkX = pieceX + overallOffset[0]
        checkY = pieceY + overallOffset [1]
        if checkX not in range(0,constants.BOARDX) or checkY not in range(0,constants.BOARDY):
          break
        pieceToCheck = self.othelloBoard[checkY][checkX]
        if pieceToCheck == pieceColor:
          flipPieces.append([checkX][checkY])
        elif pieceToCheck == oppositePieceColor:
          flipPieces.pop()
          for piece in flipPieces:
            self.othelloBoard[piece[1]][piece[0]] = oppositePieceColor
        elif pieceToCheck == constants.BLANK:
          break
        else:
          pass
    return pieceColor

  def redoMove(self):
    Coordinate = self.undoRedoMoves.getRedoMoveCoordinates()
    if Coordinate != False:
      self.placePiece(Coordinate[0],Coordinate[1],Coordinate[2])
      return Coordinate[2]
    else:
      print("Unable to redo move, no moves left to redo.")
      return False

  def getBoard(self):
    return self.othelloBoard

  def getNextMove(self):
    return self.nextMove

  def flipNextMove(self):
    self.nextMove = self._swapColor(self.nextMove)