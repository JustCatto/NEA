import constants
import copy
import globalfunctions

class Player: #The player class, never initialised directly, instead has its methods and atributes inherited into either AI or human. 
              
  def __init__(self,playerName,assignedPiece,AIStatus): #The only two inputs needed when the class is inherited are the players name, and the assigned piece. 
    self.playerName = playerName
    self.assignedPiece = assignedPiece
    self.AIStatus = AIStatus

  def getAIStatus(self):
    return self.AIStatus
    
  def _printBoard(self,othelloBoard): #Used to print the current state of the board.
    print(" ", end = " ") #Prints a blank space to compensate for the side indicators.
    for x in range(constants.BOARDX):  
      print(x + 1, end = " ") # #Prints out the top X indicators.
    print(" ") 
    for y in range(constants.BOARDY):
      print(y + 1, end = " ") #Prints out the side Y indicators.
      for x in range(constants.BOARDX):
        print(othelloBoard[y][x],end = " ") #Prints out each row of the board.
      print(" ") #Prints a new line to ensure that the next print statement isnt on the same line as the last board row.

  def _findPiece(self,othelloBoard,piece): #Method used to find all of one particular color on the grid and return the list with all their coordinates on it.
    coordinateList = []
    for x in range(constants.BOARDX): #Cycles through all positions on the board.
      for y in range(constants.BOARDY): 
        if othelloBoard[y][x] == piece: #Selects a piece from the board, if they match with the queried color, the coordiantes are appended to a list.
          coordinateList.append([x,y])
    return coordinateList #Once all positions on the board are searched, returns the coordinate list.

  def getTotalPieces(self,othelloBoard): #Method used to find all friendly pieces on the grid and return the number that there are.
    totalPieces = 0
    for x in range(constants.BOARDX): #Cycles through all positions on the board.
      for y in range(constants.BOARDY):
        if othelloBoard[y][x] == self.assignedPiece: #Selects a piece from the board. If it is the classes assigned piece, the totalPieces variable has 1 added to it.
          totalPieces += 1
    return totalPieces #Once all positions on the board are searched, returns the number of friendly pieces on the board.

  def _swapColor(self,color): #Method to swap the color of the queried piece (For example, BLACK returns WHITE, WHITE returns BLACK.)
    if color == constants.BLACK: #If the color is BLACK, WHITE is returned.
      return constants.WHITE
    elif color == constants.WHITE: #If the color is WHITE, BLACK is returned.
      return constants.BLACK
    else:
      globalfunctions.reportError(0) #If the method was called erroniously, and is neither white or black, a general error is returned to the user to alert them of this.
      return False

  def _getPossibleMoves(self,othelloBoard,Friendly): #Gets all of the possible moves of one specific color.
    if Friendly == True: #If the getPossibleMoves method is searching for all possible friendly moves, the piece to be used is the assigned piece.
      piece = self.assignedPiece
      oppositePiece = self._swapColor(self.assignedPiece)
    else: #If it is searching for all possible enemy moves, the piece to be used is the enemy piece, or the assignedPiece passed through the swapColor method.
      piece = self._swapColor(self.assignedPiece) 
      oppositePiece = self.assignedPiece
    offsets = constants.OFFSETS #Loads up the offsets from the constants file.
    possibleMoves = [] #Initialises the possibleMoves list so that it can be appended to.
    pieceCoordinates = self._findPiece(othelloBoard,piece) #Finds all of the pieces of the one specific color.
    for coordinate in pieceCoordinates: #Cycles through all of the coordinates.
      for offset in offsets: #Cycles through all of the offsets in the offsets list.
        oppositePiecesInPath = 0 #Initialises/resets the oppositePiece counter whenever a new direction is being searched.
        overallOffset = copy.copy(offset) #Makes a copy of the offset and saves it as the total offset.
        while True: #Loops as long as there isnt an enemy piece or a blank piece.
          checkX = coordinate[0] + overallOffset[0] #Creates the coordinates to be searched by adding the original coordinates
          checkY = coordinate[1] + overallOffset[1] #And the offset together.
          if checkX not in range(0,constants.BOARDX) or checkY not in range(0,constants.BOARDY): #If the coordinate to be searched is out of the boards range, break the loop.
            break
          pieceToCheck = othelloBoard[checkY][checkX] #If it is in range, get the piece to be searched from the board.
          if pieceToCheck == constants.BLANK: #If the piece is blank, the oppositePiece counter isnt 0, and the coordinate is already not in possible moves, append it to the list.
            if oppositePiecesInPath != 0 and [checkX,checkY] not in possibleMoves:
              possibleMoves.append([checkX,checkY])
            break
          elif pieceToCheck == oppositePiece: #If it is an opposite piece, add one to the counter and add the original offset to the total offset to search the next piece.
            oppositePiecesInPath += 1
            overallOffset[0] += offset[0]
            overallOffset[1] += offset[1] 
          elif pieceToCheck == piece: #If the piece to be searched is friendly, break the loop to search the next direction
            break
          else: #If the piece doesnt match any of the conditions, return an error to the user and break the loop direction.
            globalfunctions.reportError(0)
            break
    return possibleMoves #Returns the possible moves list once all directions have been searched.
        