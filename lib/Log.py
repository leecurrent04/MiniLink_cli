import os
import datetime

name_history : dict = {}

def saveLog(name:str, data:str):
    if(os.path.isdir("./log") == False):
        os.makedirs("./log")

    if name not in list(name_history.keys()):
        now = datetime.datetime.now().strftime('%Y-%m-%d(%H_%M_%S)')
        file_name : str = f"{now}-{name}.txt"

        name_history.update({name:file_name})
    else :
        file_name = name_history[name]
    
    with open(f"./log/{file_name}", 'a') as fp:
        fp.write(data)
        fp.write('\n')


def saveLogFromList(name:str, data:list, isHex=False):
    now = datetime.datetime.now().strftime('%Y-%m-%d(%H_%M_%S)')

    if(isHex == False):
        log :str = f"[{now}],{','.join(map(str,data))}"
    else:
        log :str = f"[{now}],"
        for i in data:
            log = log + "%02x,"%i

    saveLog(name, log)