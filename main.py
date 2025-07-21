import os
import keyboard
from lib.userChooseHandler import UserChooseHandler

from lib.MAVLink import *


 
port, baudrate, msg = UserChooseHandler.chooseInit()
mav = MAVLink(port, baudrate, msg)

while True:
    mav.getData()
    if keyboard.is_pressed('q'): break
    if keyboard.is_pressed('s'): 
        mav.setLog(UserChooseHandler.choose_msg())
