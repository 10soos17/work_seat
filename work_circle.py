#!/usr/bin/python3
import cgi, os
import time

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
