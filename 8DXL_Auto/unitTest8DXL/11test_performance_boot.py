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

class TestPerformanceBoot:
    @pytest.fixture(autouse=True)
    def setup(self, request, cfg):
        #sall the paramaters got from config.yaml
        self.config = cfg
        from common import log
        from common import image_download
        self.image = image_download.ImageDownload(self.config['UUU']['path'])
        self.com_cm4 = serialspawn.SerialSpawn(self.config['COM']['CM4'], self.config['COM']['CM4_baudrate'])
        self.com_uboot = serialspawn.SerialSpawn(self.config['COM']['uBoot'], self.config['COM']['uBoot_baudrate'])
        self.com_scfw = serialspawn.SerialSpawn(self.config['COM']['SCFW'], self.config['COM']['SCFW_baudrate'])
        self.bcu = bcu.BCU(self.config['BCU']['port'], self.config['BCU']['baudrate'])
        self.bcu.set_boot_device('sdp')
        self.bcu.reset()
        
        def teardown():
            self.bcu.set_boot_device('none')
            self.bcu.reset()
            self.bcu.close()
            self.com_cm4.close()
            self.com_uboot.close()
            self.com_scfw.close()
        request.addfinalizer(teardown)
        
    @pytest.mark.parametrize('par',['flexspi_cm4_ddr_1M_uboot','flexspi_cm4_ddr_2M_uboot','flexspi_cm4_ddr_3M_uboot','flexspi_cm4_flexspi_1M_uboot','flexspi_cm4_flexspi_2M_uboot','flexspi_cm4_flexspi_3M_uboot'])
    def test_flexspi_performance_boot(self,par):
        #download image
        self.image.download_image('test_flexspi_performance_boot{}'.format(par), 'flexspi_performance', SDPimage=self.config['Image']['serial_download'], 
                                    bootImage1=self.config['Image'][par])
        logging.info('------------------Flexspi TestPerformanceBoot boot {}-------------------'.format(par))
        #set boot device then reset
        self.bcu.set_boot_device('flexspi')
        self.bcu.reset()
        #clear console buffer
        self.com_cm4.clear_buffer()
        self.com_uboot.clear_buffer()
        self.com_scfw.clear_buffer()
        #checking boot expectation
        self.com_scfw.find('Debug Monitor', timeout = 5)
        self.com_uboot.find('Hit any key to stop autoboot', timeout = 5)
        self.com_cm4.find('hello world Flexspi', timeout = 10)


if __name__ == '__main__':
    import subprocess
    pytest = os.path.abspath(os.path.join(sys.executable, '..', 'Scripts', 'py.test.exe'))
    cmd = ['test_performance_boot.py::TestPerformanceBoot::test_flexspi_performance_boot']
    subprocess.call([pytest, '-v' ,'-s', cmd])