#Used to store general purpose functions that are required in all of the classes.
from time import sleep
import sys
import constants
def typing(w): #Might use this but tbh not any of my stuff needs this kind of thing
  for i in w:
    sleep(0.04)
    sys.stdout.write(i)
    sys.stdout.flush()

def reportError(error):
  try:
    print(constants.errorCodes[error])
  except KeyError:
    print("Unknown error-Errorcode does not exist")
  finally:
    print("Continuing may have unintended consequences. You are advised to shut off the program and check your savefile to avoid corruption.")