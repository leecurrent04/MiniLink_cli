import serial.tools.list_ports
import questionary

from .MiniLink import MiniLink

class UserChooseHandler():
    port = None;
    baudrate = None
    msg = None

    def chooseInit():
        cl = UserChooseHandler
        try:
            cl.port = cl.__choose_port_init()
            cl.baudrate = cl.__choose_buadrate_init()
            # cl.msg = cl.__choose_msg_init()

        except Exception as err:
            print(err)
            cl.chooseInit()

        return [cl.port, cl.baudrate]

    def choose_port(addition_item=None):
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

    def choose_buadrate(addition_item):
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


    def choose_msg(handlerDict:dict, addition_item=None):
        lists = [f"{handler[0]} : {handler[1][0]}" for handler in list(handlerDict.items())]

        if(addition_item!=None) :
            lists.append(addition_item)

        answer = questionary.select(
            "Choose MSG :",
            choices = lists
        ).ask()

        if addition_item != None and answer in addition_item:
            return answer

        return int(answer.split(" : ")[0])


    def __choose_port_init():
        cl = UserChooseHandler
        answer = cl.choose_port("a) EXIT")

        if(answer == "a) EXIT") : exit()

        return answer.split(" - ")[0]

    def __choose_buadrate_init():
        cl = UserChooseHandler

        answer = cl.choose_buadrate(["a) MANNUAL INPUT", "b) ../"])
        match(answer):
            case "a) MANNUAL INPUT" :
                try:
                    answer = int(input("INPUT baudrate :"))
                    return int(answer)
                except Exception as err:
                    print(err)
            case "b) ../":
                cl.port = cl.__choose_port_init()

            case _:
                return int(answer)

        return cl.__choose_buadrate_init()

    # def __choose_msg_init():
    #     cl = UserChooseHandler

    #     answer = cl.choose_msg("a) ../")

    #     if(answer=="a) ../"):
    #         cl.port = cl.__choose_buadrate_init()
    #         return cl.__choose_buadrate_init()

    #     return answer

        

