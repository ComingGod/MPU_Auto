#coding:utf-8
#pip install pyserial

# import log
import serial
import logging
import time
import pexpect
from pexpect.spawnbase import SpawnBase


class SerialSpawn(SpawnBase):
    """docstring for Ser"""
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=0.5)

        super(SerialSpawn, self).__init__(
        3,
        searchwindowsize=None,
        logfile=None,
        encoding=None,
        codec_errors='strict'
        )

    def read_nonblocking(self, size=1, timeout=None):
        s = self.ser.readline()
        return s

    def send(self, s):
        self.ser.write(s)

    def find(self, pattern, timeout):
        try:
            self.expect(pattern, timeout)
            logging.info(self.before + self.after)
            return self.before + self.after
        except pexpect.EOF:
            logging.info('Boot failed')
            return None

    def catch(self, pattern, timeout):
        try:
            self.expect(pattern+'.*\n', timeout)
            logging.info(self.before + self.after)
            return (self.after).split(pattern)[1]
        except pexpect.EOF:
            return None

    def close(self):
        self.ser.close()



        

if __name__ == "__main__": 
    # port = 'com28'
    # baudrate = '115200'
    spawn = SerialSpawn('COM28', 115200)
    spawn.find('Debug Monitor', timeout = 5)
    print spawn.after
    spawn.send('seco info\n')
    spawn.find('UID.*\n', 5)
  
    spawn.close()





  