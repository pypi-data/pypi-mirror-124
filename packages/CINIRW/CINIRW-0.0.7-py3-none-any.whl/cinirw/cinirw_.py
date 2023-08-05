# -*- coding: utf-8 -*-

import configparser

# CreateConfigIni 创建Ini的封装
# ReadConfigIni 读取Ini的封装
# WriteConfigIni 写入Ini的封装


##
# CreateConfigIni
##

class CreateConfigIni():
    def __init__(self, filename):
        self.cf = configparser.ConfigParser()
        self.__filename__ = filename

    def parseConfig(self, section, key, val):
        self.cf.set(section, key, val)
        self.cf.write(open(self.__filename__, "w"))

    def createConfigSection(self, section):
        self.cf.add_section(section)

##
# ReadConfigIni
##

class ReadConfigIni():
    def __init__(self, filename):
        self.cf = configparser.ConfigParser()
        self.cf.read(filename)

    def getConfigValue(self, section, name):
        value = self.cf.get(section, name)
        # print(value)
        return value

##
# WriteConfigIni
##

class WriteConfigIni():
    def __init__(self, filename):
        self.cf = configparser.ConfigParser()
        self.__filename__ = filename

    def putConfigValue(self, section, key, val):
        self.cf.set(section, key, val)
        self.cf.write(open(self.__filename__, "w"))

    def addConfigSection(self, section):
        self.cf.add_section(section)


if __name__ == '__main__':
    ROOT = 'TestcaseFeedPool'
    pathd = "." + os.sep + ROOT + os.sep + "config_devices_draft_SN12345678.ini"
    DoConfigIni = ReadConfigIni(pathd)
    Address = DoConfigIni.getConfigValue("LocationInformation", "Address")
    print("Address: ", Address)
    #
    pathd2 = "." + os.sep + ROOT + os.sep + "config_devices_test_SN12345678.ini"
    UpdateConfigIni = WriteConfigIni(pathd2)
    UpdateConfigIni.putConfigValue("LocationInformation", "Lattitude", "new lattitude")
