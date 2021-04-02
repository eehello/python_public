import tkinter.messagebox   #这个是消息框，对话框的关键
import tkinter.filedialog   #文件打开对话框
import os                   #文件目录相关
import datetime             #获取系统时间
import windnd               #文件拖拽使用,需安装windnd
import win32api             #释放DLL动态库使用,需安装pywin32
 
from tkinter import *
from tkinter import ttk     #下拉菜单使用
from tkinter.scrolledtext import ScrolledText
from ctypes import *
from sys import version
 
'''
#请使用命令"pip install windnd"  安装windnd库
#请使用命令"pip install pywin32" 安装pywin32库
'''
 
#初始化编码选择下拉框和文件打开按钮
def InitCRCCalcParam():
    global FileName
    CRC_value.set('')
    if 1 == CalcType.get():
        LoadFile.place_forget()
        contents.config(state=NORMAL) #打开文本输入框编辑状态
        contents.delete(1.0, END)
        contents.insert(1.0,'请输入字符串')
        contents.insert(END,'\n\n启用C库=OFF 使用Pyhon计算CRC,速度较慢。')
        contents.insert(END,'\n启用C库=On  使用C语言计算，速度极快，但需\n            本目录下的CrcCalc.dll文件。')
        contents.insert(END,'\n\n\n\n')
        contents.insert(END,'\n\nemail：forlover521@vip.qq.com')
        contents.config(bg = 'white')
        cmb_CodeType.place(x=60*2, y=0, width=60, height=24)
        cmb_CodeType_desc.place(x=60*3, y=0, width=96, height=24)
        FileName = ''
    else:
        LoadFile.place(x=60*2, y=0, width=60, height=24)
        contents.delete(1.0, END)
        contents.insert(1.0,'请拖拽文件到本窗口或通过[打开]按钮载入。')
        contents.insert(END,'\n\n启用C库=OFF 使用Pyhon计算CRC,速度较慢。')
        contents.insert(END,'\n启用C库=On  使用C语言计算，速度极快，但需\n            本目录下的CrcCalc.dll文件。')
        contents.insert(END,'\n\n注：将整个文件一次性加载至内存，因此不适合\n    计算大文件(50MB文件测试通过)。若需计算\n    大文件，请自行修改代码，使用分段计算。')
        contents.insert(END,'\n\nemail：forlover521@vip.qq.com')
        contents.config(state=DISABLED) #关闭文本输入框编辑状态
        contents.config(bg = 'gainsboro')
        cmb_CodeType.place_forget()
        cmb_CodeType_desc.place_forget()
    return 0
 
#初始化C语言库选择框状态
def InitCLibEnable():
    global DllFileName
    if -1 != version.find('32 bit'):
        DllFileName='CrcCalc.dll'
        print('32位Pyhon')
    else:
        DllFileName='CrcCalc64.dll'
        print('64位Pyhon')
    if DllFileName in os.listdir(os.path.abspath('.')):
        CLibCheck.config(state=NORMAL) #正常编辑状态
    else:
        CLibEnable.set(0)
        CLibCheck.config(state=DISABLED) #禁用状态
    return 0
 
def Contents_ScrolledText_Set():
    global FileName
    global FileSize
    FileSize = os.path.getsize(FileName)
    contents.config(state=NORMAL) #打开文本输入框编辑状态
    contents.delete(1.0, END)
    contents.insert(1.0, FileName)  #也是从文本头插入
    contents.insert(END, '\n文件大小=%d字节'%FileSize)   #也是从文本尾插入
    contents.config(state=DISABLED) #关闭文本输入框编辑状态
    return FileName
 
def OpenFile():
    global FileName
    global FileSize
    FileName_t  = tkinter.filedialog.askopenfilename()    #取消后是返回一个空字符串
    if not FileName_t:
        FileSize_t = 0
        print("未选择文件")
    else:
        FileName = FileName_t
        Contents_ScrolledText_Set()
    return FileName
 
def Dragged_file(files):
    global FileName
    global FileSize
    FileName = str(files[0], encoding = "gbk")  #windows默认编码为gbk，win10不知道是不是改成utf-8了
    Contents_ScrolledText_Set()
    return FileName
 
def Print_Radiobutton():
    print("CalcTypeg=%d:" % CalcType.get(), end="")
    if 1 == CalcType.get():
        print("计算字符串CRC  ", end="")
        print("%s编码" % cmb_CodeType.get())
    else:
        print("计算文件CRC  ")
    InitCRCCalcParam()
    return 0
 
 
def CrcCalc16_XMODEM(Buffer, Len):
    wCRCin = 0x0000
    wCPoly = 0x1021
    for j in range(Len):
        char = Buffer[j]
        wCRCin ^= ((char << 8) & 0xffff)
        for i in range(8):
            if(wCRCin & 0x8000):
                wCRCin = ((wCRCin << 1) ^ wCPoly) & 0xffff
            else:
                wCRCin = (wCRCin << 1) & 0xffff
    return wCRCin
 
def CrcCalc32(Buffer, Len):
    CRC32table = [
    0x00000000, 0x77073096, 0xee0e612c, 0x990951ba, 0x076dc419, 0x706af48f, 0xe963a535, 0x9e6495a3,
    0x0edb8832, 0x79dcb8a4, 0xe0d5e91e, 0x97d2d988, 0x09b64c2b, 0x7eb17cbd, 0xe7b82d07, 0x90bf1d91,
    0x1db71064, 0x6ab020f2, 0xf3b97148, 0x84be41de, 0x1adad47d, 0x6ddde4eb, 0xf4d4b551, 0x83d385c7,
    0x136c9856, 0x646ba8c0, 0xfd62f97a, 0x8a65c9ec, 0x14015c4f, 0x63066cd9, 0xfa0f3d63, 0x8d080df5,
    0x3b6e20c8, 0x4c69105e, 0xd56041e4, 0xa2677172, 0x3c03e4d1, 0x4b04d447, 0xd20d85fd, 0xa50ab56b,
    0x35b5a8fa, 0x42b2986c, 0xdbbbc9d6, 0xacbcf940, 0x32d86ce3, 0x45df5c75, 0xdcd60dcf, 0xabd13d59,
    0x26d930ac, 0x51de003a, 0xc8d75180, 0xbfd06116, 0x21b4f4b5, 0x56b3c423, 0xcfba9599, 0xb8bda50f,
    0x2802b89e, 0x5f058808, 0xc60cd9b2, 0xb10be924, 0x2f6f7c87, 0x58684c11, 0xc1611dab, 0xb6662d3d,
    0x76dc4190, 0x01db7106, 0x98d220bc, 0xefd5102a, 0x71b18589, 0x06b6b51f, 0x9fbfe4a5, 0xe8b8d433,
    0x7807c9a2, 0x0f00f934, 0x9609a88e, 0xe10e9818, 0x7f6a0dbb, 0x086d3d2d, 0x91646c97, 0xe6635c01,
    0x6b6b51f4, 0x1c6c6162, 0x856530d8, 0xf262004e, 0x6c0695ed, 0x1b01a57b, 0x8208f4c1, 0xf50fc457,
    0x65b0d9c6, 0x12b7e950, 0x8bbeb8ea, 0xfcb9887c, 0x62dd1ddf, 0x15da2d49, 0x8cd37cf3, 0xfbd44c65,
    0x4db26158, 0x3ab551ce, 0xa3bc0074, 0xd4bb30e2, 0x4adfa541, 0x3dd895d7, 0xa4d1c46d, 0xd3d6f4fb,
    0x4369e96a, 0x346ed9fc, 0xad678846, 0xda60b8d0, 0x44042d73, 0x33031de5, 0xaa0a4c5f, 0xdd0d7cc9,
    0x5005713c, 0x270241aa, 0xbe0b1010, 0xc90c2086, 0x5768b525, 0x206f85b3, 0xb966d409, 0xce61e49f,
    0x5edef90e, 0x29d9c998, 0xb0d09822, 0xc7d7a8b4, 0x59b33d17, 0x2eb40d81, 0xb7bd5c3b, 0xc0ba6cad,
    0xedb88320, 0x9abfb3b6, 0x03b6e20c, 0x74b1d29a, 0xead54739, 0x9dd277af, 0x04db2615, 0x73dc1683,
    0xe3630b12, 0x94643b84, 0x0d6d6a3e, 0x7a6a5aa8, 0xe40ecf0b, 0x9309ff9d, 0x0a00ae27, 0x7d079eb1,
    0xf00f9344, 0x8708a3d2, 0x1e01f268, 0x6906c2fe, 0xf762575d, 0x806567cb, 0x196c3671, 0x6e6b06e7,
    0xfed41b76, 0x89d32be0, 0x10da7a5a, 0x67dd4acc, 0xf9b9df6f, 0x8ebeeff9, 0x17b7be43, 0x60b08ed5,
    0xd6d6a3e8, 0xa1d1937e, 0x38d8c2c4, 0x4fdff252, 0xd1bb67f1, 0xa6bc5767, 0x3fb506dd, 0x48b2364b,
    0xd80d2bda, 0xaf0a1b4c, 0x36034af6, 0x41047a60, 0xdf60efc3, 0xa867df55, 0x316e8eef, 0x4669be79,
    0xcb61b38c, 0xbc66831a, 0x256fd2a0, 0x5268e236, 0xcc0c7795, 0xbb0b4703, 0x220216b9, 0x5505262f,
    0xc5ba3bbe, 0xb2bd0b28, 0x2bb45a92, 0x5cb36a04, 0xc2d7ffa7, 0xb5d0cf31, 0x2cd99e8b, 0x5bdeae1d,
    0x9b64c2b0, 0xec63f226, 0x756aa39c, 0x026d930a, 0x9c0906a9, 0xeb0e363f, 0x72076785, 0x05005713,
    0x95bf4a82, 0xe2b87a14, 0x7bb12bae, 0x0cb61b38, 0x92d28e9b, 0xe5d5be0d, 0x7cdcefb7, 0x0bdbdf21,
    0x86d3d2d4, 0xf1d4e242, 0x68ddb3f8, 0x1fda836e, 0x81be16cd, 0xf6b9265b, 0x6fb077e1, 0x18b74777,
    0x88085ae6, 0xff0f6a70, 0x66063bca, 0x11010b5c, 0x8f659eff, 0xf862ae69, 0x616bffd3, 0x166ccf45,
    0xa00ae278, 0xd70dd2ee, 0x4e048354, 0x3903b3c2, 0xa7672661, 0xd06016f7, 0x4969474d, 0x3e6e77db,
    0xaed16a4a, 0xd9d65adc, 0x40df0b66, 0x37d83bf0, 0xa9bcae53, 0xdebb9ec5, 0x47b2cf7f, 0x30b5ffe9,
    0xbdbdf21c, 0xcabac28a, 0x53b39330, 0x24b4a3a6, 0xbad03605, 0xcdd70693, 0x54de5729, 0x23d967bf,
    0xb3667a2e, 0xc4614ab8, 0x5d681b02, 0x2a6f2b94, 0xb40bbe37, 0xc30c8ea1, 0x5a05df1b, 0x2d02ef8d]
 
    crc=0xffffffff;
    
    for j in range(Len):
        crc = (((crc>>8)^CRC32table[(crc^Buffer[j])&0xff])&0xffffffff);
    crc = (crc^0xffffffff)
    return crc
 
def DealDLL():
    global CrcCalcDLL
    global DllFileName
    if 1==CLibEnable.get():
        if DllFileName in os.listdir(os.path.abspath('.')):
            CrcCalcDLL = cdll.LoadLibrary('./'+DllFileName)
            print('已加载动态库:',os.path.abspath('.')+'\\'+DllFileName)
        else:
            tkinter.messagebox.showwarning('警告','没有找到CrcCalc.dll')
            CLibEnable.set(0)
    else:
        win32api.FreeLibrary(CrcCalcDLL._handle)
    return 0
 
def LinkCrcCalcFunc(buffer, Len):
    if 'CRC16' == cmb_CRCType.get():
        if 0 == CLibEnable.get():   #如果不启用dll动态库
            CRC = (CrcCalc16_XMODEM(buffer, Len) & 0xffff)
        else:
            CRC = (CrcCalcDLL.GetCRC16(buffer,Len) & 0xffff)
        CRC_value.set("0x%04X" % CRC)
        
    if 'CRC32' == cmb_CRCType.get():
        if 0 == CLibEnable.get():   #如果不启用dll动态库
            CRC = (CrcCalc32(buffer, Len)& 0xffffffff)
        else:
            CRC = (CrcCalcDLL.GetCRC32(buffer,Len) & 0xffffffff)
        CRC_value.set("0x%08X" % CRC)
            
    return CRC
 
def CRCClac():
    global FileName
    global FileSize
    CRC = 0x0
    if 1 == CalcType.get(): #计算字符串
        if 'UTF8' == cmb_CodeType.get():
            buffer = contents.get(0.0, END).encode('utf-8')
        if 'GBK' == cmb_CodeType.get():
            buffer = contents.get(0.0, END).encode('gbk')
        FileSize = len(buffer)-1
        CRC=LinkCrcCalcFunc(buffer,FileSize)
    else:   #计算文件
        if not FileName:
            tkinter.messagebox.showwarning('警告','亲，请先选择文件~')
        elif 0 == FileSize:
            tkinter.messagebox.showwarning('警告','亲，请正确选择文件~')
        else:
            contents.config(state=NORMAL) #打开文本输入框编辑状态
            time = datetime.datetime.now().strftime('%T')
            contents.insert(END, '\n%s 开始计算CRC'%time)   #也是从文本尾插入
            with open(FileName, 'rb') as file:
                buffer = file.read(FileSize)
                CRC=LinkCrcCalcFunc(buffer,FileSize)
            time = datetime.datetime.now().strftime('%T')
            contents.insert(END, '\n%s 计算完成CRC=0x%X'%(time,CRC))   #也是从文本尾插入
            contents.config(state=DISABLED) #关闭文本输入框编辑状态
        
    print("CRC=0x%08X" % CRC)
    return CRC
 
top = Tk()
top.title("CRC计算工具")
top.geometry("322x234")
 
FileName=''
FileSize=0
CrcCalcDLL=None
DllFileName = 'CrcCalc.dll'
 
#CRC计算按钮
ClacCrc = Button()
ClacCrc.config(text='CRC计算', command=CRCClac)
ClacCrc.place(x=2, y=26, width=60, height=24)
 
#下拉菜单
cmb_CRCType = ttk.Combobox(state="readonly")
cmb_CRCType.place(x=64, y=26, width=64, height=24)
cmb_CRCType['value'] = ('CRC16','CRC32')
cmb_CRCType.current(0)
Label(text="=").place(x=130, y=26, width=16, height=24)
 
#CRC显示框
CRC_value = StringVar()
CRCVal = Entry(textvariable = CRC_value)
CRCVal.place(x=146, y=26, width=90, height=24)
 
#字符串输入框，文件路径输入框
contents = ScrolledText()
contents.place(x=2, y=52, width=320, height=180)
 
#计算类型选择单选
CalcType = IntVar()
CalcType.set(2)
radio_Str = Radiobutton(text="字符串",anchor="w", variable=CalcType, value=1, command=Print_Radiobutton)
radio_File = Radiobutton(text="文件",anchor="w", variable=CalcType, value=2, command=Print_Radiobutton)
radio_Str.place(x=0, y=0, width=60, height=24)
radio_File.place(x=60*1, y=0, width=60, height=24)
 
#编码选择下拉框
cmb_CodeType = ttk.Combobox(state="readonly")
cmb_CodeType.place(x=60*2, y=0, width=60, height=24)
cmb_CodeType['value'] = ('GBK','UTF8')
cmb_CodeType.current(0)
cmb_CodeType_desc = Label(text="(字符串编码格式)")
cmb_CodeType_desc.place(x=60*3, y=0, width=96, height=24)
 
#打开文件按钮
LoadFile = Button()
LoadFile.config(text='打开', command=OpenFile)
 
#初始化编码选择和打开文件按钮
InitCRCCalcParam()
 
#采用内置函数还是C动态库
CLibEnable = IntVar()
CLibEnable.set(0)
CLibCheck = Checkbutton(top, text = "使用C库", variable = CLibEnable, onvalue=1, offvalue=0, command=DealDLL)
CLibCheck.place(x=236, y=26, width=90, height=24)
#初始化C库选择
InitCLibEnable()
 
#拖放文件函数
windnd.hook_dropfiles(top, func=Dragged_file)
 
mainloop()
