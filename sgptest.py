import smbus2
from smbus2 import SMBusWrapper, SMBus, i2c_msg
from collections import namedtuple 
from functools import partial
#import Adafruit_PureIO.smbus as adabus
from time import sleep, asctime,time
import json
from copy import copy
import requests
import os.path

DEVICE_BUS = 1
DEVICE_ADDR = 0x58
BASELINE_FILENAME = os.path.expanduser("~/sgp_config_data.txt")
#print bus.write_byte_datadata(DEVICE_ADDR, 0x00, 0x01)
#self._i2c_read_words_from_cmd([0x36, 0x82], 0.01, 3)

Sgp30Cmd = namedtuple("Sgp30Cmd",["commands","replylen","waittime"])
GET_SERIAL=Sgp30Cmd([0x36, 0x82],6,10)
GET_FEATURES=Sgp30Cmd([0x20, 0x15],2,2)
IAQ_INIT=Sgp30Cmd([0x20, 0x03],0,10)
IAQ_MEASURE=Sgp30Cmd([0x20, 0x08],6,12)
IAQ_SELFTEST=Sgp30Cmd([0x20, 0x32],3,520)
GET_BASELINE=Sgp30Cmd([0x20, 0x15],6,120)
SET_BASELINE=Sgp30Cmd([0x20, 0x1e],0,10)

Sgp30Answer = namedtuple("Sgp30Answer",["data","raw"])

def read_write(cmd,bus,addr=DEVICE_ADDR):
    write = i2c_msg.write(addr,cmd.commands)
    if cmd.replylen <= 0 :
       bus.i2c_rdwr(write)
    else:
        read = i2c_msg.read(addr,cmd.replylen)
        bus.i2c_rdwr(write) 
        sleep(waittime/1000.0)
        bus.i2c_rdwr(read)
        r = list(read)
        answer = [i<<8 | j for i,j in zip(r[0::3],r[1::3])]
        return Sgp30Answer(answer,r)

def try_set_baseline():
    try:
        with open(BASELINE_FILENAME,"w") as conf:
            baseline=json.load(conf)
            baseline_cmd = copy(SET_BASELINE)
            baseline_cmd.commands += baseline
    except IOError:
        pass
    except ValueError:
        pass
    else:
        if len(baseline) == 6:
            print("Loading baseline data into sensor")
            rw(baseline_cmd)

def init_sgp(bus):
    print("Initializing SGP30")
    rw(IAQ_INIT)
    print("Waiting for sensor warmup")
    try_set_baseline()
    #print(rw(SET_BASELINE))
    sleep(15)

def i2c_geral_call(bus):
    print("resetting bus")
    bus.write_byte(0,0x06)
    sleep(.1)

def store_baseline(n):
    if (n > 3600 * 12) and (n % 3600 == 3599):
        with open(BASELINE_FILENAME,"w") as conf:
            baseline= rw(GET_BASELINE)
            json.dump(baseline.raw,conf)

with SMBusWrapper(1) as bus:
    rw=partial(read_write,bus=bus)
    print(rw(GET_FEATURES))
    print(rw(GET_SERIAL))
    print(rw(IAQ_INIT))
    #print(rw(IAQ_SELFTEST,sleep_time=.1))
    for i in range(600):
        print( "CO_2eq: %d ppm, TVOC: %d"%tuple( rw(IAQ_MEASURE,sleep_time=.1)))
        sleep(2)
    

bus.close()
