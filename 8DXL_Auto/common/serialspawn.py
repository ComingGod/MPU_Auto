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
        #add delay for opening the serial
        time.sleep(0.1)

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
            logging.info('--------Finding {}---------'.format(pattern))
            logging.info(self.before + self.after)
            return self.before + self.after
        except pexpect.EOF:
            logging.info('Boot failed')
            assert 1 == 0
            return None

    def catch(self, pattern, timeout):
        try:
            self.expect(pattern+'.*\n', timeout)
            logging.info(self.before + self.after)
            return (self.after).split(pattern)[1]
        except pexpect.EOF:
            return None

    #clean all the input/output buffer for uart
    def clear_buffer(self):
        time.sleep(0.1)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        logging.info('-------------Clear console buffer---------------')

    def read_all(self):
        time.sleep(0.1)
        print self.ser.read(self.ser.in_waiting)

    def close(self):
        self.ser.close()


if __name__ == "__main__": 
    # port = 'com28'
    # baudrate = '115200'
    spawn = SerialSpawn('COM24', 115200)
    spawn.send('reset\n')
    spawn.clear_buffer()
    print '---------------------------'
    spawn.read_all()
    print '---------------------------'


    spawn.send('reset\n')
    spawn.read_all()

  
    spawn.close()





  