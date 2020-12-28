#!/usr/bin/python3
import cgi, os
import time
<<<<<<< HEAD
import threading
=======
>>>>>>> 59fe7905be1f5e6cc928c6912bc794f737069be3

def current_time():
    currentdate =  time.strftime("%Y / %m / %d")
    localtime =  time.strftime("%H:%M:%S")
    morning = 5<= int(time.strftime("%H")) <12
    afternoon = 12<=int(time.strftime("%H"))<19
    evening = 19<=int(time.strftime("%H"))<24 or 0<=int(time.strftime("%H"))<5
    if morning:
        return str(f"Good morning\n{currentdate}\n{localtime}")
    elif afternoon:
        return str(f"Good afternoon\n{currentdate}\n{localtime}")
    elif evening:
        return str(f"Good evening\n{currentdate}\n{localtime}")
