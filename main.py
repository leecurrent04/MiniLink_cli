from lib.MiniLink import MiniLink
from lib.userInputHandler import UserInputHandler

mav = MiniLink()
userInput = UserInputHandler()

port, baudrate = userInput.chooseInit()

mav.connect(port, baudrate)
mav.setMSG_ID(userInput.choose_msgInit(mav.readMSGList()))

while True:
    retVal = userInput.whileInputHandler()
    if retVal != None:
        mav.setMSG_ID(retVal)

    # True or False
    data : list = mav.readData(enPrint=True, enLog=True)

    # Edit Here
    # If you want to access value
    # if(data != None):
    #     print(data)

