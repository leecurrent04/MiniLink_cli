import sys
import serial
import numpy

from lib.xmlHandler import XmlHandler
from lib.Log import *

MINILINK_VERSION = 0xFA

class MiniLink():
    xmlHandler = XmlHandler()

    # {id:[name, addr, count]}
    msgs_dict : dict= {}
    msgs_dict_ori : dict= {}

    packet = {
        'data' : numpy.zeros(1024, int), 
        'Header' : 0, 'Length' : 0, 'SEQ' : 0, 'MSG ID' : 0, 'CRC' : 0
    }

    ser:serial = None
    __cnt:int = 0
    __MSG_ID = None

    def __init__(self):
        self.xmlHandler.loadMSGList(self.msgs_dict_ori)

    def getMSGList(self):
        return self.msgs_dict

    def readMSGList(self):
        print("[MiniLink] loading messages list")
        while 1:
            if(self.readByte(self.packet) != 0): continue
            data : numpy.array = self.packet['data']
            msg_id = data[3] | data[4] << 8

            self.packet['SEQ'] = data[2]
            self.packet['MSG ID'] = msg_id

            if(msg_id in list(self.msgs_dict.keys())):
                return self.msgs_dict

            self.msgs_dict.update({msg_id:self.msgs_dict_ori[msg_id]})

    # 한 패킷을 받아서 출력
    def readData(self, isPrint=None):
        if(self.readByte(self.packet) != 0): return None

        data : numpy.array = self.packet['data']
        length : int = self.packet['Length']
        msg_id = data[3] | data[4] << 8

        self.packet['SEQ'] = data[2]
        self.packet['MSG ID'] = msg_id

        if(msg_id not in list(self.msgs_dict.keys())):
            self.msgs_dict.update({msg_id:self.msgs_dict_ori[msg_id]})

        self.msgs_dict[msg_id][2] = self.msgs_dict[msg_id][2] +1

        saveLogFromList("packet-raw", data, isHex=True)
        saveLogFromList(f"{self.msgs_dict[msg_id][0]}", self.xmlHandler.parser(msg_id, data[5:length-2], False))

        if(self.__MSG_ID != self.packet['MSG ID']) :
            return None

        return self.xmlHandler.parser(self.__MSG_ID, data[5:length-2], isPrint)

    def connect(self, port, baudrate=115200, MSG_ID=None):
        try:
            self.ser = serial.Serial(port, baudrate)
            self.__cnt = 0
            print("[%s %d] Connected!"%(port, baudrate))

            if(MSG_ID != None):
                self.setMSG_ID(MSG_ID)

            self.readMSGList()
            return 0

        except Exception as err:
            print(err)
            exit()

    def setMSG_ID(self, id):
        self.__MSG_ID = id
        return

    # byte 단위로 데이터 받아옴
    def readByte(self, packet:dict):
        try:
            data : numpy.array = packet['data']

            rx_byte = self.ser.read()  # 1바이트씩 읽기

            if(self.__cnt >= len(data)):
                print("Must increase Buffer size! %d"%(len(data)))
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

        rxCRC = data[length-2]| data[length-1]<<8
        retval = self.calulate_crc(data, length)

        return retval == rxCRC

    def calulate_crc(self, data, length):
        crc = 0x0000
        for i in range(0, length -2):
            crc ^= (data[i] << 8)
            for j in range(0, 8):
                if (crc & 0x8000):
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc = (crc << 1)

        return crc&0xffff

    def byte2int(self, x):
        return int("0x"+str(x),16)
