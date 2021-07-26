import threading
import time
import serial
import opendoor
import closedoor
import binascii
import re
import struct


class SerThread:
    def __init__(self, Port, Baud, Bytesize, Stopbits):
        # 初始化串口、blog文件名称
        self.receiveCount = 0
        self.my_serial = serial.Serial()
        self.my_serial.port = Port
        self.my_serial.baudrate = Baud
        self.my_serial.bytesize = Bytesize
        self.my_serial.stopbits = Stopbits
        self.my_serial.timeout = 1
        self.alive = False
        self.waitEnd = None
        fname = time.strftime("%Y%m%d")  # blog名称为当前时间
        self.rfname = 'r' + fname  # 接收blog名称
        self.sfname = 's' + fname  # 发送blog名称
        self.thread_read = None
        self.thread_send = None

    def waiting(self):
        # 等待event停止标志
        if not self.waitEnd is None:
            self.waitEnd.wait()

    def start(self):
        # 开串口以及blog文件
        self.rfile = open(self.rfname, 'w')
        self.sfile = open(self.sfname, 'w')
        self.my_serial.open()

        if self.my_serial.isOpen():
            self.waitEnd = threading.Event()
            self.alive = True

            self.thread_send = threading.Thread(target=self.Sender)
            self.thread_send.setDaemon(True)

            self.thread_read = threading.Thread(target=self.Reader)
            self.thread_read.setDaemon(True)

            self.thread_send.start()
            self.thread_read.start()

            return True
        else:
            return False

    def asciiB2HexString(self, strB):
        strHex = binascii.b2a_hex(strB).upper()
        return re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", strHex.decode()) + " "

    def hex_to_float(self, h):
        i = int(h, 16)
        return struct.unpack('<f', struct.pack('<I', i))[0]

    def Reader(self):
        while self.alive:
            try:
                while True:
                    length = max(1, min(4096, self.my_serial.in_waiting))
                    time.sleep(1)
                    bytes = self.my_serial.read(length)
                    if bytes is not None:
                        self.receiveCount += len(bytes)
                        data = self.asciiB2HexString(bytes)
                        print('recv' + ' ' + time.strftime("%Y-%m-%d %X"))
                        print(data.strip())
                        list1 = []
                        for a in data:
                            list1.append(a)
                        a1 = list1[15]
                        a2 = list1[16]
                        a3 = list1[18]
                        a4 = list1[19]
                        a5 = list1[9]
                        a6 = list1[10]
                        a7 = list1[12]
                        a8 = list1[13]
                        data1 = a1 + a2 + a3 + a4 + a5 + a6 + a7 + a8
                        # print(data1)
                        data = self.hex_to_float(data1)
                        print(f'辐射值为：{data}')
                        if data is None:
                            pass
                        else:
                            if data > 100:
                                #door.opendoor()
                            elif data <= 100:
                                #door.closedoor()
                            else:
                                print("保持！")
                        print('recv' + ' ' + time.strftime("%Y-%m-%d %X") + ' ' + data.strip())
                        print(time.strftime("%Y-%m-%d %X:") + data.strip(), file=self.rfile)
                        if len(data) == 1 and ord(data[len(data) - 1]) == 113:  # 收到字母q，程序退出
                            break
            except Exception as ex:
                print('')

        self.waitEnd.set()
        self.alive = False

    def Sender(self):
        while self.alive:
            try:
                snddata = bytes.fromhex('01 03 00 15 00 02 D5 CF')
                self.my_serial.write(snddata)
                time.sleep(1)
                print('sent' + ' ' + time.strftime("%Y-%m-%d %X"))
                print(snddata)
            except Exception as ex:
                print(ex)

        self.waitEnd.set()
        self.alive = False

    def stop(self):
        self.alive = False
        # self.thread_read.join()
        # self.thread_send.join()
        if self.my_serial.isOpen():
            self.my_serial.close()
        self.rfile.close()
        self.sfile.close()


if __name__ == '__main__':

    ser = SerThread('com11', 9600, 8, 2)
    try:
        if ser.start():
            ser.waiting()
            ser.stop()
        else:
            pass
    except Exception as ex:
        print(ex)

    if ser.alive:
        ser.stop()

    print('End OK .')
    del ser
