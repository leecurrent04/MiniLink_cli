import os
import keyboard

from lib.userChooseHandler import UserChooseHandler
from lib.MiniLink import MiniLink

mav = MiniLink()
port, baudrate = UserChooseHandler.chooseInit()
mav.connect(port, baudrate)
mav.setMSG_ID(UserChooseHandler.choose_msg(mav.readMSGList()))

while True:
    if keyboard.is_pressed('q'): break
    if keyboard.is_pressed('s'): 
        mav.setMSG_ID(UserChooseHandler.choose_msg())

    # Edit Here
    data : list = mav.readData(isPrint=True)

    # If you want to access value
    # if(data != None):
    #     print(data)

