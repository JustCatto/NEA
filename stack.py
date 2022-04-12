class Stack:
  def __init__(self):
    self.contents = []
    self.topOfStackPointer = 0

  def _isEmpty(self):
    if self.contents == []:
      return True
    else:
      return False

  def pushCoordinates(self,x,y,piece):
    if self.topOfStackPointer != len(self.contents):
      newList = []
      for x in range(self.topOfStackPointer):
        newList.append(self.contents[x-1])
      self.contents = newList
    self.topOfStackPointer += 1
    self.contents.append([x,y,piece])
  
  def getUndoMoveCoordinates(self):
    if self._isEmpty() == False and self.topOfStackPointer > 0:
      Parse = self.contents[self.topOfStackPointer-1]
      self.topOfStackPointer -= 1
      return [Parse[0],Parse[1],Parse[2]]
    return False

  def getRedoMoveCoordinates(self):
    if self._isEmpty() == False and len(self.contents) > self.topOfStackPointer:
      self.topOfStackPointer += 1
      Parse = self.contents[self.topOfStackPointer-1]
      return [Parse[0],Parse[1],Parse[2]]
    else:
      return False

  def getStackLength(self):
    return len(self.contents)

  def getStackPointer(self):
    return self.topOfStackPointer

  def getStackContents(self):
    return self.contents