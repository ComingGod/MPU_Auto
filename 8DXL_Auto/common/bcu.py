#coding:utf-8
#pip install pyserial

import serial
import logging
import time
import pexpect
from pexpect.spawnbase import SpawnBase


# class BCU(SpawnBase):
#     """docstring for Ser"""
#     def __init__(self, port, baudrate):
#         self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=0.5)

#         super(BCU, self).__init__(
#         3,
#         searchwindowsize=None,
#         logfile=None,
#         encoding=None,
#         codec_errors='strict'
#         )

#     def read_nonblocking(self, size=1, timeout=None):
#         s = self.ser.readline()
#         return s


#     def find(self, pattern, timeout):
#         try:
#             self.expect(pattern, timeout)
#             logging.info(self.before + self.after)
#             return self.before + self.after
#         except pexpect.EOF:
#             logging.info('Boot failed')
#             return None

#     def reset(self):
#         logging.info('---------------reset board---------------')
#         self.ser.write('RESET_BOARD\n')
#         self.find('Finish command', 5)

#     def set_boot_device(self, device):
#         #001 for SDP
#         if device == 'sdp':
#             logging.info('---------------set serial download mode---------------')
#             self.ser.write('IN1_HIGH\n')
#             self.find('Finish command', 1)
#             time.sleep(0.5)
#             self.ser.write('IN2_LOW\n')
#             self.find('Finish command', 1)
#             time.sleep(0.5)
#             self.ser.write('IN3_LOW\n')
#             self.find('Finish command', 1)
#         #011 for SD
#         elif device == 'sd':
#             logging.info('---------------set sd boot---------------')
#             self.ser.write('IN1_HIGH\n')
#             self.find('Finish command', 1)
#             time.sleep(0.5)
#             self.ser.write('IN2_HIGH\n')
#             self.find('Finish command', 1)
#             time.sleep(0.5)
#             self.ser.write('IN3_LOW\n')
#             self.find('Finish command', 1)
#         #010 for emmc
#         elif device =='emmc':
#             logging.info('---------------set emmc boot---------------')
#             self.ser.write('IN1_LOW\n')
#             self.find('Finish command', 1)
#             time.sleep(0.5)
#             self.ser.write('IN2_HIGH\n')
#             self.find('Finish command', 1)
#             time.sleep(0.5)
#             self.ser.write('IN3_LOW\n')
#             self.find('Finish command', 1)
#         #110 for flexspi
#         elif device == 'flexspi':
#             logging.info('---------------set flexspi boot---------------')
#             self.ser.write('IN1_LOW\n')
#             self.find('Finish command', 1)
#             time.sleep(0.5)
#             self.ser.write('IN2_HIGH\n')
#             self.find('Finish command', 1)
#             time.sleep(0.5)
#             self.ser.write('IN3_HIGH\n')
#             self.find('Finish command', 1)
#     def close(self):
#         self.ser.close()


class BCU(object):
    """docstring for Ser"""
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=0.5)
        #add delay for opening the serial
        time.sleep(0.1)
    def reset(self):
        logging.info('---------------reset board---------------')
        self.ser.write('RESET_BOARD\n')
        time.sleep(0.5)
        logging.info(self.ser.readlines())

    def set_boot_device(self, device):
        #001 for SDP
        if device == 'sdp':
            logging.info('---------------set serial download mode---------------')
            self.ser.write('IN1_HIGH\n')
            time.sleep(0.5)
            logging.info(self.ser.readlines())
            self.ser.write('IN2_LOW\n')
            time.sleep(0.5)
            logging.info(self.ser.readlines())
            self.ser.write('IN3_LOW\n')
            time.sleep(0.5)
            logging.info(self.ser.readlines())        
            #011 for SD
        elif device == 'sd':
            logging.info('---------------set sd boot---------------')
            self.ser.write('IN1_HIGH\n')
            time.sleep(0.5)
            logging.info(self.ser.readlines())
            self.ser.write('IN2_HIGH\n')
            time.sleep(0.5)
            logging.info(self.ser.readlines())
            self.ser.write('IN3_LOW\n')
            time.sleep(0.5)
            logging.info(self.ser.readlines())
        #010 for emmc
        elif device =='emmc':
            logging.info('---------------set emmc boot---------------')
            self.ser.write('IN1_LOW\n')
            time.sleep(0.5)
            logging.info(self.ser.readlines())
            self.ser.write('IN2_HIGH\n')
            time.sleep(0.5)
            logging.info(self.ser.readlines())
            self.ser.write('IN3_LOW\n')
            time.sleep(0.5)
            logging.info(self.ser.readlines())
        #110 for flexspi
        elif device == 'flexspi':
            logging.info('---------------set flexspi boot---------------')
            self.ser.write('IN1_LOW\n')
            time.sleep(0.5)
            logging.info(self.ser.readlines())
            self.ser.write('IN2_HIGH\n')
            time.sleep(0.5)
            logging.info(self.ser.readlines())
            self.ser.write('IN3_HIGH\n')
            time.sleep(0.5)
            logging.info(self.ser.readlines())
        #000 set all the pin as low voltage
        elif device == 'none':
            logging.info('---------------set boot pin as None---------------')
            self.ser.write('IN1_LOW\n')
            time.sleep(0.5)
            logging.info(self.ser.readlines())
            self.ser.write('IN2_LOW\n')
            time.sleep(0.5)
            logging.info(self.ser.readlines())
            self.ser.write('IN3_LOW\n')
            time.sleep(0.5)
            logging.info(self.ser.readlines())
    def close(self):
        self.ser.close()


if __name__ == "__main__": 
    # port = 'com28'
    # baudrate = '115200'
    bcu = BCU('COM5', 115200)
    bcu.set_boot_device('flexspi')
    bcu.reset()
    bcu.close()
  





  