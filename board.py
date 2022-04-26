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

  def _swapColor(self,color): #Method that flips the color that is input. For example if black is input, return white, and vice versa.
    if color == constants.BLACK:
      return constants.WHITE
    elif color == constants.WHITE:
      return constants.BLACK
    else:
      globalfunctions.reportError(0) #If the function is improperly called, return an error.
      return False

  def generateBoard(self): #Method that generates the board and places down the starting pieces.
    self.othelloBoard = [[constants.BLANK for x in range(constants.BOARDX)]for y in range(constants.BOARDY)] #Initialises the board using the dimentions in the constants file.
    self.piece = constants.BLACK 
    for x in range(2): #These lines are then responsible for placing the starting pieces.
      self.piece = self._swapColor(self.piece) 
      for y in range(2):
        self.othelloBoard[y+3][x+3] = self.piece 
        self.piece = self._swapColor(self.piece) 
    self.nextMove = constants.WHITE

  def placePiece(self,x,y,piece): #Method that places down the piece at the specified coordinates and flips any pieces that become directly surrounded by the piece and another friendly piece.
    offsets = constants.OFFSETS #Loads the offsets from the constants file.
    self.othelloBoard[y][x] = piece #Sets the spot at the specified coordinates to the piece.
    oppositePiece = self._swapColor(piece) #Finds the opposite piece by swapping the color of the originally specified piece.
    self.undoRedoMoves.pushCoordinates(x,y,piece) #Pushes coordinates to the undoRedoMove stack so then it may be undone.
    for offset in offsets: #Cycles through all the offsets.
      flipPieces = [] #Clears the flipPieces list each time to make sure no coordinates are carried over.
      overallOffset = copy.copy(offset) #Takes a copy of the current offset and stores it as the total offset.
      while True: #Loops while the pieces that are being scanned are not friendly pieces or blank pieces.
        checkY = y + overallOffset[1] #Adds the original coordinates plus the offsets to find the coordinates to search.
        checkX = x +overallOffset[0]
        if checkY not in range(0,constants.BOARDY) or checkX not in range(0,constants.BOARDX): #If the coordinates to search arent in range of the board, break the loop and search in another direction.
          break
        pieceToCheck = self.othelloBoard[checkY][checkX] #Get the value of the piece at the coordinates to scan.
        if pieceToCheck == piece: #If the piece is friendly, flip all the pieces in the flipPieces list.
          for flipPiece in flipPieces:
            self.othelloBoard[flipPiece[1]][flipPiece[0]] = piece
          break
        elif pieceToCheck == constants.BLANK: #If the piece is blank, clear the flipPieces list and break the while True loop as there can be no pieces to flip in this direction.
          flipPieces = []
          break
        elif pieceToCheck == oppositePiece: #If the piece is an enemy piece, log the coordinates down in the flipPieces list and add the original offset to the total offset.
          flipPieces.append([checkX,checkY])
          overallOffset[1] += offset[1]
          overallOffset[0] += offset[0]

  def undoMove(self): #Method to undo the last done move.
    Coordinate = self.undoRedoMoves.getUndoMoveCoordinates() #Gets the coordinates from the stack
    if Coordinate == False: #If the stack returns false, there are no moves left to undo and therefore it is displayed
      print("Unable to undo move, no moves left to undo.")
      return False
    offsets = constants.OFFSETS #Loads the offsets from the constants file.
    pieceX = Coordinate[0] #Breaks down the coordinate list output to x,y and piece.
    pieceY = Coordinate[1]
    pieceColor = Coordinate[2]
    oppositePieceColor = self._swapColor(pieceColor) #Gets the oppositeColor by swapping the color of the pieceColor variable.
    self.othelloBoard[pieceY][pieceX] = constants.BLANK #Sets the specified coordinates to blank.
    for offset in offsets: #Cycles through all of the offsets.
      flipPieces = [] #Clears/Initialises the flipPieces list.
      overallOffset = copy.copy(offset) #Copies the offset into the overallOffset variable.
      while True: #this loop is broken if the piece is blank, or if an enemy piece is found.
        checkX = pieceX + overallOffset[0] #Adds the offset and original coordinates together to get the coordinates of the spot to search.
        checkY = pieceY + overallOffset [1]
        if checkX not in range(0,constants.BOARDX) or checkY not in range(0,constants.BOARDY): #If the coordinates of the spot to search are out of range of the board, break the loop and search in another direction.
          break
        pieceToCheck = self.othelloBoard[checkY][checkX] #If the coordinates are in range, get the value of the piece at the specified coordinates 
        if pieceToCheck == pieceColor: #If the piece is friendly, ammend this to the flipPieces list.
          flipPieces.append([checkX,checkY])
          overallOffset[0] += offset[0]
          overallOffset[1] += offset[1] 
        elif pieceToCheck == oppositePieceColor: #If the piece is an enemy piece, remove the last coordinate from the flipPieces list and flip all the pieces to be enemy pieces.
          if len(flipPieces) > 0:
            flipPieces.pop()
            for piece in flipPieces: 
              self.othelloBoard[piece[1]][piece[0]] = oppositePieceColor
          break
        elif pieceToCheck == constants.BLANK: #If the piece is blank, break the loop.
          if len(flipPieces) > 0:
            flipPieces.pop()
            for piece in flipPieces: 
              self.othelloBoard[piece[1]][piece[0]] = oppositePieceColor
        else: 
          globalfunctions.reportError(0)
          return False
    return pieceColor #Once all the directions have been searched, return the original piece color.

  def redoMove(self): #Method to redo the last undone move
    Coordinate = self.undoRedoMoves.getRedoMoveCoordinates() #Gets the coordinates from the stack
    if Coordinate != False: #As long as the coordinate is not false, attempt to place the piece as normal and return the original color of that piece.
      self.placePiece(Coordinate[0],Coordinate[1],Coordinate[2])
      return self._swapColor(Coordinate[2])
    else: #If the coordinate is false, return False and display to the user that there are no moves left to undo.
      print("Unable to redo move, no moves left to redo.")
      return False

  def getBoard(self):
    return self.othelloBoard

  def getNextMove(self):
    return self.nextMove

  def flipNextMove(self):
    self.nextMove = self._swapColor(self.nextMove)

  def getStackContents(self):
    return self.undoRedoMoves.getStackContents()