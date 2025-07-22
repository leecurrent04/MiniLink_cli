import sys
import serial
import numpy

from lib.xmlHandler import XmlHandler
from lib.Log import *

MINILINK_VERSION = 0xFA
CLI_NAME = "MiniLink"

class MiniLink():
    xmlHandler = XmlHandler()

    # {id:[name, addr, count]}
    msgs_dict : dict= {}
    msgs_dict_ori : dict= {}

    packet = {
        'Header' : 0, 'Length' : 0, 'SEQ' : 0, 'MSG ID' : 0, 
        'data' : numpy.zeros(1024, int), 
        'CRC' : 0
    }

    ser:serial = None
    __cnt:int = 0
    __MSG_ID = None

    def __init__(self):
        self.xmlHandler.loadMSGList(self.msgs_dict_ori)

    # connect
    # @detail : 새로운 장치에 연결
    def connect(self, port, baudrate=115200, MSG_ID=None):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            self.__cnt = 0
            print(f"[{CLI_NAME}] Connected to %s (%d)"%(port, baudrate))

            if(MSG_ID != None):
                self.chooseMessage(MSG_ID)

            self.readMessageList()

            print(f"[{CLI_NAME}] Press 'm' key to open the memu.")
            return 0

        except Exception as err:
            print(err)
            exit()


    # chooseMessage()
    # @detail : 화면에 표시할 메세지를 선택함
    def chooseMessage(self, id):
        if id not in list(self.msgs_dict.keys()):
            print(f"[{CLI_NAME}] invaild message id");
            return -1

        print(self.xmlHandler.getTitle(id))
        self.__MSG_ID = id

        return


    # getMessageList()
    # @detail : 장치에서 전송하는 MSG 목록를 리턴
    def getMessageList(self):
        return self.msgs_dict


    # readMessageList()
    # @detail : 장치에서 전송하는 MSG 목록을 받아옴.
    def readMessageList(self):
        try:
            print(f"[{CLI_NAME}] Loading the messages...")

            while 1:
                if(self.__readByte(self.packet) != 0): continue
                data : numpy.array = self.packet['data']
                msg_id:int= data[3] | data[4] << 8

                self.packet['SEQ'] : int = data[2]
                self.packet['MSG ID'] : int = msg_id

                if(msg_id in list(self.msgs_dict.keys())):
                    print(f"[{CLI_NAME}] Found {len(list(self.msgs_dict.keys()))} messages!")
                    return self.msgs_dict

                self.msgs_dict.update({int(msg_id):self.msgs_dict_ori[msg_id]})

        except Exception as err:
            print(err)


    # read()
    # @detail : 한 패킷을 받아서 출력
    def read(self, enPrint:bool=False, enLog:bool=False):
        if(self.__readByte(self.packet) != 0): return None

        data : numpy.array = self.packet['data']
        length : int = self.packet['Length']
        msg_id = data[3] | data[4] << 8

        self.packet['SEQ'] = data[2]
        self.packet['MSG ID'] = msg_id

        if(msg_id not in list(self.msgs_dict.keys())):
            self.msgs_dict.update({msg_id:self.msgs_dict_ori[msg_id]})

        self.msgs_dict[msg_id][2] = self.msgs_dict[msg_id][2] +1

        # Log
        if(enLog == True):
            saveLogFromList("packet-raw", data[:length], isHex=True)
            saveLogFromList("msg_frequency", [i[2] for i in self.msgs_dict.values()], header=[i[0] for i in self.msgs_dict.values()])
            saveLogFromList(f"{self.msgs_dict[msg_id][0]}", self.xmlHandler.parser(msg_id, data[5:length-2]), header=self.xmlHandler.getTitle(msg_id))

        # print or return only selected value 
        if(self.__MSG_ID != self.packet['MSG ID']) :
            return None

        unpacked_data:list = self.xmlHandler.parser(self.__MSG_ID, data[5:length-2])

        if(enPrint == True):
            print(unpacked_data)

        return unpacked_data


    # send()
    # @detail : message 전송
    # @parm : data : list [MSG ID, [Payload]]
    def send(self, data : list):
        try:
            self.packet['SEQ'] = self.packet['SEQ'] + 1

            tx : list = [MINILINK_VERSION]
            tx.append(7+len(data[1]))
            tx.append(int(self.packet['SEQ']))
            tx = tx + [(int(data[0]) & 0xff), (int(data[0]) >> 8)]
            tx = tx + data[1]

            crc = int(self.calculate_crc(tx, len(tx)+2))
            tx = tx + [(crc >> 8), (crc & 0xff)]

            self.ser.write(bytes(tx))
            print(f"[{CLI_NAME}] send : ", tx)

        except Exception as err:
            print(err)


    # __readByte()
    # @detail : byte 단위로 데이터 받아옴
    def __readByte(self, packet:dict):
        try:
            data : numpy.array = packet['data']

            rx_byte = self.ser.read()  # 1바이트씩 읽기
            if(rx_byte == b''): return 2;

            if(self.__cnt >= len(data)):
                print(f"{CLI_NAME} Have to increase Buffer size! {len(data)}")
                self.__cnt = 0

            data[self.__cnt] = self.byte2int(rx_byte.hex())

            match(self.__cnt):
                case 0 : 
                    if data[self.__cnt] not in [MINILINK_VERSION, 0xFD, 0xFE] :
                        self.__cnt = 0
                        return -1;
                case 1 : 
                    packet['Length'] = data[self.__cnt]
                case _:
                    if(self.__cnt == packet['Length'] -1):
                        self.__cnt = 0
                        if(packet['Length']>0 and self.checkCRC()):
                            return 0
                        return 1;
                    elif (self.__cnt > packet['Length'] -1) :
                        return -1;

            self.__cnt = self.__cnt + 1


        except Exception as e:
            print(e)
            sys.exit(0)

        return 1


    def checkCRC(self):
        length : int= self.packet['Length']
        data : numpy.array = self.packet['data']

        rxCRC = data[length-1]<<8 | data[length-2] 
        retval = self.calculate_crc(data, length)

        return retval == rxCRC


    def calculate_crc(self, data, length):
        crc:numpy.uint16 = 0x0000
        for i in range(0, length -2):
            crc ^= numpy.uint16(data[i] << 8)
            for j in range(0, 8):
                if (crc & 0x8000):
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc = (crc << 1)

        return crc&0xffff


    def byte2int(self, x):
        return int("0x"+str(x),16)

