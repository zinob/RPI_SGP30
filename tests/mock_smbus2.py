from collections import namedtuple 

from .context import sgp30
from time import time
import sys

I2CAnswers= namedtuple("I2CAnswers",["answer","min_delay"])
I2A = I2CAnswers
def add_crc(l):
    return l + [sgp30.Crc8().hash(l)]

if sys.version_info[0] < 3:
    byte_from_int = chr
else:
    byte_from_int = lambda x: bytes([x])

answers = {
    (0x36, 0x82): I2A(add_crc([0,0]),.4), #GET_SERIAL
    (0x20, 0x15): I2A(add_crc([0,0]), 1), #GET_FEATURES
    (0x20, 0x03): I2A(None, 2), #IAQ_INIT
    (0x20, 0x08): I2A([1, 144, 76, 0, 6, 39], 10), #IAQ_MEASURE
    (0x20, 0x32): I2A(add_crc([0xD4,0x00]), 200), #IAQ_SELFTEST
    (0x20, 0x15): I2A([133, 152, 85, 138, 32, 202], 10), #GET_BASELINE
    (0x20, 0x1e): I2A(None, 10) #SET_BASELINE
}

class MockSMBus:
    def __init__(s,break_crc=False):
        s.status=None
        s.last=None
        s.addr=None
        s._break_crc=break_crc
        s._deadline=time() 

    def _set_deadline(s, t):
        s._deadline=time() + t/1000.

    def i2c_rdwr(s,*msgs):
        for m in msgs:
            if time() < s._deadline:
                raise IOError("To fast buss-access, device not ready")
            if m.flags == 1:
                s._process_read(m)
            else:
                s._process_write(m)

    def write_byte(s,addr,data):
        s.status=None
        s.addr=addr
        s.last=data

    def _process_read(s,msg):
        if s.status == None:
            raise AssertionError("Tried to read before write")
        for i in range(len(s.status)):
            msg.buf[i]=byte_from_int(s.status[i])
            if s._break_crc and i%3 == 2:
                msg.buf[i]=byte_from_int(s.status[i]^42)
        s.status=None
                

    def _process_write(s,msg):
        a = answers[tuple(msg)[0:2]]
        s._set_deadline(a.min_delay)
        s.status = a.answer
        s.last=msg
    
