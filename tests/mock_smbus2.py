from smbus2 import i2c_msg

from .context import sgp30

def add_crc(l):
    return l + [sgp30.Crc8().hash(l)]

answers = {
    (0x36, 0x82): add_crc([0,0]) ,#GET_SERIAL
    (0x20, 0x15): add_crc([0,0]) ,#GET_FEATURES
    (0x20, 0x03): None ,#IAQ_INIT
    (0x20, 0x08): [1, 144, 76, 0, 6, 39] ,#IAQ_MEASURE
    (0x20, 0x32): add_crc([0xD4,0x00]),#IAQ_SELFTEST
    (0x20, 0x15): add_crc([0x00,0x00])*2 ,#GET_BASELINE  Invalid, should be more realistic data..
    (0x20, 0x1e): None,#SET_BASELINE
}

class MockSMBus:
    def __init__(s):
        s.status=None

    def i2c_rdwr(s,*msgs):
        for m in msgs:
            if m.flags == 1:
                s._process_read(m)
            else:
                s._process_write(m)
    def _process_read(s,msg):
        if s.status == None:
            raise AssertionError("tired to read before write")
        for i in range(len(s.status)):
            msg.buf[i]=chr(s.status[i])
    def _process_write(s,msg):
        s.status = answers[tuple(msg)]
    
