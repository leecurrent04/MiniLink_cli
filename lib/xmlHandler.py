import os
import numpy
import struct
import xml.etree.ElementTree as ET

class XmlHandler:
    fp = None
    root = None
    msgs_dict : dict = None

    def __init__(self):
        self.__loadXML()

    # xml file load
    def __loadXML(self):
        self.fp = open("lib/MSG/common.xml", 'r')
        self.root = ET.fromstring(self.fp.read())


    # load all msg list (ex. SCALED_IMU)
    def loadMSGList(self, msgs:dict):
        self.msgs_dict = msgs
        messages = self.root.find("messages").findall("message")

        for msg in messages:
            msgs.update({int(msg.get("id")):[msg.get("name"), msg, 0]})

        return msgs


    # get key of values (ex. SCALED_IMU.xacc)
    def getTitle(self, id):
        data : list = []
        fields = self.msgs_dict[id][1].findall("field")

        for field in fields:
            data.append(field.get("name"))

        return data


    def parser(self, id, rx:numpy.array):
        try:
            fields = self.msgs_dict[id][1].findall("field")

            fmt : str = '<'
            for field in fields:
                match(field.get("type")):
                    case 'uint64_t': fmt=fmt+"Q"
                    case 'uint32_t': fmt=fmt+"I"
                    case 'uint16_t': fmt=fmt+"H"
                    case 'uint8_t': fmt=fmt+"B"

                    case 'int64_t': fmt=fmt+"q"
                    case 'int32_t': fmt=fmt+"i"
                    case 'int16_t': fmt=fmt+"h"
                    case 'uint8_t': fmt=fmt+"b"

                    case 'float': fmt=fmt+"f"
                    case 'double': fmt=fmt+"d"

            unpacked_data : list = list(struct.unpack(fmt, bytes(list(rx))))

            return unpacked_data

        except Exception as err:
            print(f"{err} ({len(rx)}) : ")
            for i in rx: print("%02x "%(i), end= '')
            print("")
            
