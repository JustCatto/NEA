#Used to store general purpose functions that are required in all of the classes.
from time import sleep
import sys
import constants
def typing(w):
  for i in w:
    sleep(0.01)
    sys.stdout.write(i)
    sys.stdout.flush()
  print("\n")

def reportError(error):
  try:
    print(constants.errorCodes[error])
  except KeyError:
    print("Unknown error-Errorcode does not exist")
  finally:
    print("Continuing may have unintended consequences. You are advised to shut off the program and check your savefile to avoid corruption.")