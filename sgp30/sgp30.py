import smbus2
from smbus2 import SMBusWrapper, SMBus, i2c_msg
from collections import namedtuple 
from functools import partial
from time import sleep, asctime,time
import json
from copy import copy
import requests
import os.path

DEVICE_BUS = 1
BASELINE_FILENAME = os.path.expanduser("~/sgp_config_data.txt")

class _commands():
    """container class for mapping between human readable names and the command values used by the sgp"""
    Sgp30Cmd = namedtuple("Sgp30Cmd",["commands","replylen","waittime"])
    GET_SERIAL=Sgp30Cmd([0x36, 0x82],6,10)
    GET_FEATURES=Sgp30Cmd([0x20, 0x15],2,2)
    IAQ_INIT=Sgp30Cmd([0x20, 0x03],0,10)
    IAQ_MEASURE=Sgp30Cmd([0x20, 0x08],6,12)
    IAQ_SELFTEST=Sgp30Cmd([0x20, 0x32],3,520)
    GET_BASELINE=Sgp30Cmd([0x20, 0x15],6,120)
    SET_BASELINE=Sgp30Cmd([0x20, 0x1e],0,10)

    @classmethod
    def new_set_baseline(cls,baseline_data):
        baseline_cmd = copy(cls.SET_BASELINE)
        baseline_cmd.commands += baseline_data
        return baseline_cmd

class Sgp30():

    def __init__(self,bus,device_address = 0x58):
        self._bus = bus
        self._device_addr = device_address
        self.rw=partial(read_write,bus=bus)
        self._start_time = time()

    Sgp30Answer = namedtuple("Sgp30Answer",["data","raw"])

    def read_write(self,cmd):
        write = i2c_msg.write(self._device_addr,cmd.commands)
        if cmd.replylen <= 0 :
           self._bus.i2c_rdwr(write)
        else:
            read = i2c_msg.read(self._device_addr,cmd.replylen)
            bus.i2c_rdwr(write) 
            self._bus.i2c_rdwr(write) 
            bus.i2c_rdwr(read)
            self._bus.i2c_rdwr(read)
            r = list(read)
            answer = [i<<8 | j for i,j in zip(r[0::3],r[1::3])]
            return Sgp30Answer(answer,r)

    def try_set_baseline():
        try:
            with open(BASELINE_FILENAME,"w") as conf:
                baseline_cmd = _commands.new_set_baseline(json.load(conf))
        except IOError:
            pass
        except ValueError:
            pass
        else:
            if len(baseline) == 6:
                print("Loading baseline data into sensor")
                self.rw(baseline_cmd)

    def init_sgp(self):
        print("Initializing SGP30")
        self.rw(IAQ_INIT)
        self.try_set_baseline()
        #print(rw(SET_BASELINE))
        print("Waiting for sensor warmup")

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

def store_baseline(n):
    if (n > 3600 * 12) and (n % 3600 == 3599):
        with open(BASELINE_FILENAME,"w") as conf:
            baseline= rw(GET_BASELINE)
            json.dump(baseline.raw,conf)

def main():
    with SMBusWrapper(1) as bus:
        rw=partial(read_write,bus=bus)
        i2c_geral_call(bus)
        print("Features: %s"%repr(rw(GET_FEATURES)))
        print("Serial: %s"%repr(rw(GET_SERIAL)))
        init_sgp(bus)
        #print(rw(IAQ_SELFTEST))
        print("Testing meassure")
        print(rw(IAQ_MEASURE))
        print("Testing meassure again")
        sleep(1)
        print("Running")
        n=0
        while(True):
            start = time()
            n+=1
            co2eq, tvoc = rw(IAQ_MEASURE).data
            res = ( "%s CO_2eq: %d ppm, TVOC: %d"%( asctime(), co2eq, tvoc ))
            print(res)
            f.write("%i %i %i \n"%(time(),co2eq,tvoc))
            store_baseline(n)
            elapsed = (time() - start)
            sleep(1 - elapsed )

    bus.close()

if __name__ == "__main__":
    main()
