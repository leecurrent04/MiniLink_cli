import os
import datetime

name_history : dict = {}

# saveLog
# @detail : 기존 로그 파일이 존재하면 추가함
def saveLog(name:str, data:str, header=None):
    try:
        if(os.path.isdir("./log") == False):
            os.makedirs("./log")

        # check log.csv already existed
        if name not in list(name_history.keys()):
            now = datetime.datetime.now().strftime('%Y-%m-%d(%H_%M_%S)')
            file_name : str = f"{now}-{name}.csv"

            name_history.update({name:file_name})

            if(header != None):
                data = f"{header}\n{data}"
        else :
            file_name = name_history[name]
        
        with open(f"./log/{file_name}", 'a') as fp:
            fp.write(data)
            fp.write('\n')

    except Exception as err:
        print(err)

# saveLogFromList
# @detail : 데이터가 list로 주어질 때, str로 변환해서 저장
def saveLogFromList(name:str, data:list, isHex=False, header:list=None):
    try:
        now = datetime.datetime.now().strftime('%Y-%m-%d(%H_%M_%S)')

        # formatting Hex
        if(isHex == False):
            log :str = f"{now},{','.join(map(str,data))}"
        else:
            log :str = f"{now},"
            for i in data:
                log = log + "%02x,"%i

        if(header!=None):
            header = f"timestamp,{','.join(header)}"

        saveLog(name, log, header)

    except Exception as err:
        print(err)
