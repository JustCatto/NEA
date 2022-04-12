#Used to store general purpose functions that are required in all of the classes.
from time import sleep

def typing(w): #Might use this but tbh not any of my stuff needs this kind of thing
  for i in w:
    sleep(0.04)
    sys.stdout.write(i)
    sys.stdout.flush()