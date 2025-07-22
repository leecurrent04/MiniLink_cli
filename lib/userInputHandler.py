import sys
import keyboard
import questionary
import serial.tools.list_ports

class UserInputHandler():
    port = None;
    baudrate = None;
    msg = None;

    msgList:dict;

    flags :dict= {"print" : True, "log" : True}

    def __init__(self):
        return

    def chooseInit(self):
        try:
            self.port = self.__choose_port_init()
            self.baudrate = self.__choose_buadrate_init()
            # self.msg = self.__choose_msg_init()

        except Exception as err:
            print(err)
            self.chooseInit()

        return [self.port, self.baudrate]

    def choose_port(self, addition_item=None):
        lists = [f"{port.device} - {port.description}" for port in serial.tools.list_ports.comports()]

        if(addition_item!=None) :
            lists.append(addition_item)

        answer = questionary.select(
            "Choose Serial Port :",
            choices = lists
        ).ask()

        if answer in addition_item:
            return answer

        return answer.split(" - ")[0]

    def choose_buadrate(self, addition_item):
        lists = ['9600', '57600', '115200']

        if(addition_item!=None) :
            for i in addition_item :
                lists.append(i)

        answer = questionary.select(
            "Choose baudrate :",
            default='57600',
            choices = lists
        ).ask()

        if answer in addition_item:
            return answer

        return int(answer)


    def choose_msgInit(self, msgList:dict, addition_item=None):
        self.msgList = msgList
        return self.choose_msg(addition_item)

    def choose_msg(self, addition_item=None):
        lists = [f"{handler[0]} : {handler[1][0]}" for handler in list(self.msgList.items())]

        if(addition_item!=None) :
            lists.append(addition_item)

        answer = questionary.select(
            "Choose MSG :",
            choices = lists
        ).ask()

        if addition_item != None and answer in addition_item:
            return answer

        return int(answer.split(" : ")[0])


    def __choose_port_init(self):
        answer = self.choose_port("a) QUIT")

        if(answer == "a) QUIT") : exit()

        return answer.split(" - ")[0]

    def __choose_buadrate_init(self):
        answer = self.choose_buadrate(["a) MANNUAL INPUT", "b) ../"])

        match(answer):
            case "a) MANNUAL INPUT" :
                try:
                    answer = int(input("INPUT baudrate :"))
                    return int(answer)
                except Exception as err:
                    print(err)
            case "b) ../":
                self.port = self.__choose_port_init()

            case _:
                return int(answer)

        return self.__choose_buadrate_init()

    def whileInputHandler(self):
        if keyboard.is_pressed('q'): sys.exit()
        elif keyboard.is_pressed('s'): return self.choose_msg()
        elif not keyboard.is_pressed('m'): 
            return

        lists : list = [
            "s) Change message",
            "q) QUIT",
            "x) ../"
        ]

        answer = questionary.select(
            "MENU :",
            choices = lists
        ).ask()

        match(answer):
            case "s) Change message" :
                return self.choose_msg();
            case "q) QUIT" : sys.exit()
            case "x) ../" : return 0
        

