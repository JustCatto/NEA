class Stack:
  def __init__(self): #When the class is first initialised, create an empty stack and initialise the stack pointer as 0.
    self.contents = []
    self.topOfStackPointer = 0

  def _isEmpty(self): #Private method to check if the stack is empty before either getUndoMove or getRedoMove is called.
    if self.contents == []: #if the stack is empty, return true, else return false.
      return True
    else:
      return False

  def pushCoordinates(self,x,y,piece): #When a piece is placed, it is logged in the stack as a past move and the top of stack pointer has one added to it.
    if self.topOfStackPointer != len(self.contents): #If there are values ahead of the top of stack pointer, remove them before appending onto the stack.
      newList = []
      for x in range(self.topOfStackPointer): 
        newList.append(self.contents[x-1])
      self.contents = newList
    self.topOfStackPointer += 1  #Adds one to the topOfStackPointer.
    self.contents.append([x,y,piece]) #Appends the value onto the top of the stack.
  
  def getUndoMoveCoordinates(self): #Method to get the undo coordinates.
    if self._isEmpty() == False and self.topOfStackPointer > 0: #If the stack isnt empty and the pointer isnt already at the bottom of the stack, run the code.
      Parse = self.contents[self.topOfStackPointer-1] #Get the contents of the stack at the particular index at the stacks pointer.
      self.topOfStackPointer -= 1 #Subtracts one from the topOfStackPointer.
      return [Parse[0],Parse[1],Parse[2]] #Return the coordinates in the format x,y,color.
    else:
      return False #Returns false if the stack is full or its the back of the stack.

  def getRedoMoveCoordinates(self): #Method to get the redo coordinates.
    if self._isEmpty() == False and len(self.contents) > self.topOfStackPointer: #If the stack isnt empty and the pointer isnt already at the top of the stack, run the code.
      self.topOfStackPointer += 1 #Adds one to the stack pointer before getting the coordinates from the stack.
      Parse = self.contents[self.topOfStackPointer-1]
      return [Parse[0],Parse[1],Parse[2]] #Returns the coordinates in the format x,y,color.
    else:
      return False #Returns false if the stack is full or if the pointer is at the top of the stack.

  def getStackLength(self): #Returns the stacks current length.
    return len(self.contents)

  def getStackPointer(self): #Gets the current stack pointer position.
    return self.topOfStackPointer

  def getStackContents(self): #Gets the entire stacks contents.
    return self.contents