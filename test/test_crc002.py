

def crc16(msg01, invert=False):
    crc_reg = 0xFFFF
    ab = 0xA001
    for ii in msg01:
        crc_reg = (crc_reg>>8)^ord(ii)
        #以ii作为参数,返回对应的ASCll数值
        for i in range(8):
            check = crc_reg & 0x0001
            crc_reg >>= 1
            if (check == 0x0001):
                crc_reg ^= ab
    s = hex(crc_reg).upper()
    return s[4:6]+s[2:4] if invert == True else s[2:4]+s[4:6]
    #因s的值为十六进制的，带0X前缀，故对其切片，从第3为开始返回，默认不对返回值做颠倒处理。

    #if  invert == True:
    #    r_s = s[4:6]+s[2:4]
    #如果需对返回值先低字节码后高字节码的顺序存放，用此返回值。
    #else:
    #    r_s = s[2:4]+s[4:6]
    #如果需对返回值先高字节码后低字节码的顺序存放，用默认顺序即可，用此返回值。

#测试数据
#data001 ="QN=20191230220014171;ST=32;CN=2061;PW=123456;MN=41040001I00004;CP=&&DataTime=20191230210000;011-Min=9.088,011-Avg=9.088,011-Max=9.088,011-Cou=22.07;060-Min=2.365,060-Avg=2.365,060-Max=2.365,060-Cou=5.743;B01-Min=674.583,B01-Avg=674.583,B01-Max=674.583,B01-Cou=2428.497;065-Min=6.357,065-Avg=6.357,065-Max=6.357,065-Cou=15.438;101-Min=0.302,101-Avg=0.302,101-Max=0.302,101-Cou=0.733;001-Min=7.437,001-Avg=7.437,001-Max=7.437,001-Cou=18.061&&"
#data002 = "QN=20160801085857223;ST=32;CN=1062;PW=100000;MN=010000A8900016F000169DC0;Flag=5;CP=&&RtdInterval=30&&"
#print(crc16(data001))
#print(crc16(data001, True))
#print(crc16(data002))
#print(crc16(data002, True))

