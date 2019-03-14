# Program to demonstrate 
# timer objects in python 
  
import threading 
def gfg(): 
    print("GeeksforGeeks\n") 
  
timer = threading.Timer(2.0, gfg) 
timer.start() 
print("Exit\n")
