from smbus2 import i2c_msg

from .context import sgp30

def add_crc(l):
    return l + [sgp30.Crc8().hash(l)]

answers = {
    (0x36, 0x82): add_crc([0,0]) ,#GET_SERIAL
    (0x20, 0x15): add_crc([0,0]) ,#GET_FEATURES
    (0x20, 0x03): None ,#IAQ_INIT
    (0x20, 0x08): [1, 144, 76, 0, 6, 39] ,#IAQ_MEASURE
    (0x20, 0x32): add_crc([0xD4,0x00]) ,#IAQ_SELFTEST
    (0x20, 0x15): [133, 152, 85, 138, 32, 202] ,#GET_BASELINE
    (0x20, 0x1e): None,#SET_BASELINE
}

class MockSMBus:
    def __init__(s,break_crc=False):
        s.status=None
        s.last=None
        s.addr=None
        s._break_crc=break_crc

    def i2c_rdwr(s,*msgs):
        for m in msgs:
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
            msg.buf[i]=chr(s.status[i])
            if s._break_crc and i%3 == 2:
                msg.buf[i]=chr(s.status[i]^42)
        s.status=None
                

    def _process_write(s,msg):
        s.status = answers[tuple(msg)]
        s.last=msg
    
