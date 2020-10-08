#!/usr/bin/python3
import cgi, os
import time
import webbrowser

def current_time():
    currentdate =  time.strftime("%Y / %m / %d")
    localtime =  time.strftime("%H:%M:%S")
    morning = 5<= int(time.strftime("%H")) <12
    afternoon = 12<=int(time.strftime("%H"))<19
    evening = 19<=int(time.strftime("%H"))<24 or 0<=int(time.strftime("%H"))<5
    first = 14 <= int(time.strftime("%H")) < 15 and 10 <= int(time.strftime("%M")) <= 40
    second = 15 <= int(time.strftime("%H")) < 16 and 5 <= int(time.strftime("%M")) <= 35
    third = 16 <= int(time.strftime("%H")) < 17 and 0 <= int(time.strftime("%M")) <= 30
    fourth = (16 <= int(time.strftime("%H")) < 17 and 55 <= int(time.strftim("%M")) <= 59) or (17 <= int(time.strftime("%H")) < 18 and 0 <= int(time.strftime("%M")) <= 25) 
    middle = (18 <= int(time.strftime("%H")) < 19 and 30 <= int(time.strftime("%M")) <= 59) or (19 <= int(time.strftime("%H")) < 20 and 0 <= int(time.strftime("%M")) <= 15)
    if first:
        return str(f"1 class\n{currentdate}\n{localtime}")
    elif second:
        return str(f"2 class\n{currentdate}\n{localtime}")
    elif third:
        return str(f"3 class\n{currentdate}\n{localtime}")
    elif fourth:
        return str(f"4 class\n{currentdate}\n{localtime}")
    elif middle:
        return str(f"M class\n{currentdate}\n{localtime}")
    else: 
        return str(f"Break time!\n{currentdate}\n{localtime}")
#  if morning:
 #       return str(f"Good morning\n{currentdate}\n{localtime}")
  #  elif afternoon:
  #      return str(f"Good afternoon\n{currentdate}\n{localtime}")
  #  elif evening:
  #      return str(f"Good evening\n{currentdate}\n{localtime}")

print(current_time())
