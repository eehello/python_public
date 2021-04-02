def calc_crc(string):
    data = bytearray.fromhex(string)
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if ((crc & 1) != 0):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return hex(((crc & 0xff) << 8) + (crc >> 8))

data001 ="QN=20191230220014171;ST=32;CN=2061;PW=123456;MN=41040001I00004;CP=&&DataTime=20191230210000;011-Min=9.088,011-Avg=9.088,011-Max=9.088,011-Cou=22.07;060-Min=2.365,060-Avg=2.365,060-Max=2.365,060-Cou=5.743;B01-Min=674.583,B01-Avg=674.583,B01-Max=674.583,B01-Cou=2428.497;065-Min=6.357,065-Avg=6.357,065-Max=6.357,065-Cou=15.438;101-Min=0.302,101-Avg=0.302,101-Max=0.302,101-Cou=0.733;001-Min=7.437,001-Avg=7.437,001-Max=7.437,001-Cou=18.061&&"
crc = calc_crc(data001)
print(crc)