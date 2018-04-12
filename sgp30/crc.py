class Crc8:
    def __init__(s):
        s.crc=255

    def hash(s,int_list):
        for i in int_list:
            s.addVal(i)
        return s.crc

    def addVal(s,n):
        crc = s.crc
        for bit in range(0,8):
            if ( n ^ crc ) & 0x80:
                crc = ( crc << 1 ) ^ 0x31
            else:
                crc = ( crc << 1 )
            n = n << 1
        s.crc = crc & 0xFF
        return s.crc

#print(Crc8().hash([1,144]))
#print(hex(Crc8().hash([0xBE, 0xEF])))
#[1, 144, 76, 0, 6, 39]
