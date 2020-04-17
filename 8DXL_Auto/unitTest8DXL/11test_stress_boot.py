import pytest
import os
import sys
import logging
import Tkinter as tk

file_path = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')
main_path = os.path.abspath(os.path.join(file_path, '..')).replace('\\', '/')
sys.path.append(main_path)

from common import serialspawn
from common import bcu

class TestSDBoot:
    @pytest.fixture(autouse=True)
    def setup(self, request, cfg):
        #sall the paramaters got from config.yaml
        self.config = cfg
        from common import log
        from common import image_download
        self.image = image_download.ImageDownload(self.config['UUU']['path'])
        self.com_cm4 = serialspawn.SerialSpawn(self.config['COM']['CM4'], self.config['COM']['CM4_baudrate'])
        self.com_uboot = serialspawn.SerialSpawn(self.config['COM']['uBoot'], self.config['COM']['uBoot_baudrate'])
        self.bcu = bcu.BCU(self.config['BCU']['port'], self.config['BCU']['baudrate'])
        self.bcu.set_boot_device('sdp')
        self.bcu.reset()
        
        def teardown():
            self.bcu.set_boot_device('none')
            self.bcu.reset()
            self.bcu.close()
            self.com_cm4.close()
            self.com_uboot.close()
        request.addfinalizer(teardown)
        
    def test_sd_stress_boot(self):
        #download image
        self.image.download_image('test_sd_stress_boot', 'sd', SDPimage = self.config['Image']['serial_download'], 
                                    bootImage1 = self.config['Image']['sd_cm4_ddr_uboot'])

        for i in range(0, 1000, 1):
            logging.info('------------------SD stress boot {}-------------------'.format(i))
            #set boot device as sd then reset
            self.bcu.set_boot_device('sd')
            self.bcu.reset()
            #clear console buffer
            self.com_cm4.clear_buffer()
            self.com_uboot.clear_buffer()
            #checking boot expectation
            self.com_uboot.find('Hit any key to stop autoboot', timeout = 5)
            self.com_cm4.find('hello world SD', timeout = 10)
        
    def test_flexspi_stress_boot(self):
        #download image
        self.image.download_image('test_flexspi_stress_boot', 'flexspi', SDPimage=self.config['Image']['serial_download'], 
                                    bootImage1=self.config['Image']['flexspi_cm4_flexspi_uboot'])
        for i in range(0, 1000, 1):
            logging.info('------------------Flexspi stress boot {}-------------------'.format(i))
            #set boot device then reset
            self.bcu.set_boot_device('flexspi')
            self.bcu.reset()
            #clear console buffer
            self.com_cm4.clear_buffer()
            self.com_uboot.clear_buffer()
            #checking boot expectation
            self.com_uboot.find('Hit any key to stop autoboot', timeout = 5)
            self.com_cm4.find('hello world Flexspi', timeout = 10)

    def test_emmc_stress_boot(self):
        #download image
        self.image.download_image('test_emmc_stress_boot', 'emmc', SDPimage = self.config['Image']['serial_download'], 
                                    bootImage1 = self.config['Image']['emmc_cm4_ddr_uboot_dummy_ocram'])
        for i in range(0,1000,1):
            logging.info('------------------EMMC stress boot {}-------------------'.format(i))
            #set boot device as sd then reset
            self.bcu.set_boot_device('emmc')
            self.bcu.reset()
            #clear console buffer
            self.com_cm4.clear_buffer()
            self.com_uboot.clear_buffer()
            #checking boot expectation
            self.com_uboot.find('Hit any key to stop autoboot', timeout = 5)
            self.com_cm4.find('hello world EMMC', timeout = 10)


if __name__ == '__main__':
    import subprocess
    pytest = os.path.abspath(os.path.join(sys.executable, '..', 'Scripts', 'py.test.exe'))
    cmd = ['test_stress_boot.py::TestSDBoot::test_sd_stress_boot']
    subprocess.call([pytest, '-v' ,'-s', cmd])




