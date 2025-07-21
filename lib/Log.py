import os
import datetime

def saveLog(name:str, data:str):
    if(os.path.isdir("./log") == False):
        os.makedirs("./log")

    now = datetime.datetime.now().strftime('%Y-%m-%d(%H-%M)')
    with open(f"./log/{now}-{name}.txt", 'a') as fp:
        fp.write(data)