import smbus2
from smbus2 import SMBusWrapper, SMBus, i2c_msg
from collections import namedtuple 
from functools import partial
from time import sleep, asctime,time
import json
from copy import copy
import os.path
from .crc import Crc8

DEVICE_BUS = 1
BASELINE_FILENAME = os.path.expanduser("~/.sgp_config_data.txt")

class _cmds():
    """container class for mapping between human readable names and the command values used by the sgp"""
    Sgp30Cmd = namedtuple("Sgp30Cmd",["commands","replylen","waittime"])
    IAQ_INIT=Sgp30Cmd([0x20, 0x03],0,10)
    IAQ_MEASURE=Sgp30Cmd([0x20, 0x08],6,12)
    GET_BASELINE=Sgp30Cmd([0x20, 0x15],6,120)
    SET_BASELINE=Sgp30Cmd([0x20, 0x1e],0,10)
    SET_HUMIDITY=Sgp30Cmd([0x20, 0x61],0,10)
    IAQ_SELFTEST=Sgp30Cmd([0x20, 0x32],3,520)
    GET_FEATURES=Sgp30Cmd([0x20, 0x2f],3,3)
    GET_SERIAL=Sgp30Cmd([0x36, 0x82],9,10)

    @classmethod
    def new_set_baseline(cls,baseline_data):
        cmd = cls.SET_BASELINE
        return cls.Sgp30Cmd(cmd.commands +baseline_data,cmd.replylen,cmd.waittime)

class Sgp30():

    def __init__(self,bus,device_address = 0x58, baseline_filename=BASELINE_FILENAME):
        self._bus = bus
        self._device_addr = device_address
        self._start_time = time()
        self._last_save_time = time()
        self._baseline_filename=baseline_filename

    Sgp30Answer = namedtuple("Sgp30Answer",["data","raw","crc_ok"])
    
    def _raw_validate_crc(s,r):
        a = list(zip(r[0::3],r[1::3]))
        crc = r[2::3] == [Crc8().hash(i) for i in a ]
        return(crc,a)

    def read_write(self,cmd):
        write = i2c_msg.write(self._device_addr,cmd.commands)
        if cmd.replylen <= 0 :
           self._bus.i2c_rdwr(write)
        else:
            read = i2c_msg.read(self._device_addr,cmd.replylen)
            self._bus.i2c_rdwr(write) 
            sleep(cmd.waittime/1000.0)
            self._bus.i2c_rdwr(read)
            r = list(read)
            crc_ok,a=self._raw_validate_crc(r)
            answer = [i<<8 | j for i,j in a]
            return self.Sgp30Answer(answer,r,crc_ok)

    def store_baseline(self):
        with open(self._baseline_filename,"w") as conf:
            baseline=self.read_write(_cmds.GET_BASELINE)
            if baseline.crc_ok == True:
                json.dump(baseline.raw,conf)
                return True
            else:
                #print("Ignoring baseline due to invalid CRC")
                return False

    def try_set_baseline(self):
        try:
            with open(self._baseline_filename,"r") as conf:
                conf = json.load(conf)
        except IOError:
            pass
        except ValueError:
            pass
        else:
            crc,_ = self._raw_validate_crc(conf)
            if len(conf) == 6 and crc == True:
                self.read_write(_cmds.new_set_baseline(conf))
                return True
            else:
                #print("Failed to load baseline, invalid data")
                return False

    def read_measurements(self):
        return self.read_write(_cmds.IAQ_MEASURE)

    def read_selftest(self):
        return self.read_write(_cmds.IAQ_SELFTEST)

    def read_serial(self):
        return self.read_write(_cmds.GET_SERIAL)

    def read_features(self):
        return self.read_write(_cmds.GET_FEATURES)

    def init_sgp(self):
        #print("Initializing SGP30")
        self.read_write(_cmds.IAQ_INIT)

    def i2c_geral_call(self):
        """This attempts to reset _ALL_ devices on the i2c buss
        
        This command issues the i2c-general call RW command that should result
        in all devices aborting any read/write operations and starting to listen
        for new i2c-commands.

        This will usually un-stick the SGP30, but might reset or otherwise
        affect any device on the bus.
        """
        self._bus.write_byte(0,0x06)
        sleep(.1)


def main():
    with SMBusWrapper(1) as bus:
        sgp=Sgp30(bus,baseline_filename=BASELINE_FILENAME+".TESTING")
        print("resetting all i2c devices")
        sgp.i2c_geral_call()
        print(sgp.read_features())
        print(sgp.read_serial())
        sgp.init_sgp()
        print(sgp.read_measurements())
    bus.close()

if __name__ == "__main__":
    main()
