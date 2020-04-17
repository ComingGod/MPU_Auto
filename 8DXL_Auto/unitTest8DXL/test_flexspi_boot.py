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
from common import image_generation

class TestFlexspiBoot:
    @pytest.fixture(autouse=True)
    def setup(self, request, cfg):
        #sall the paramaters got from config.yaml
        self.config = cfg
        from common import log
        from common import image_download
        self.image = image_download.ImageDownload(self.config['UUU']['path'])
        self.gen_img = image_generation.ImageGeneration(self.config['FCB_util']['path'])
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
        
    # def test_flexspi_boot_cm4_flexspi(self):
    #     #download image
    #     self.image.download_image('test_flexspi_boot_cm4_flexspi', 'flexspi', SDPimage=self.config['Image']['serial_download'], 
    #                                 bootImage1=self.config['Image']['flexspi_cm4_flexspi'])
    #     #set boot device then reset
    #     self.bcu.set_boot_device('flexspi')
    #     self.bcu.reset()     
    #     #clear console buffer
    #     self.com_cm4.clear_buffer()
    #     self.com_uboot.clear_buffer()
    #     #checking boot expectation
    #     self.com_cm4.find('hello world Flexspi', timeout = 10)

    # def test_flexspi_boot_cm4_flexspi_uboot(self):
    #     #download image
    #     self.image.download_image('test_flexspi_boot_cm4_flexspi_uboot', 'flexspi', SDPimage=self.config['Image']['serial_download'], 
    #                                 bootImage1=self.config['Image']['flexspi_cm4_flexspi_uboot'])
    #     #set boot device then reset
    #     self.bcu.set_boot_device('flexspi')
    #     self.bcu.reset()     
    #     #clear console buffer
    #     self.com_cm4.clear_buffer()
    #     self.com_uboot.clear_buffer()
    #     #checking boot expectation
    #     self.com_uboot.find('Hit any key to stop autoboot', timeout = 5)
    #     self.com_cm4.find('hello world Flexspi', timeout = 10)

    # def test_flexspi_boot_cm4_flexspi_uboot_dummy_ocram(self):
    #     #download image
    #     self.image.download_image('test_flexspi_boot_cm4_flexspi_uboot_dummy_ocram', 'flexspi', SDPimage=self.config['Image']['serial_download'], 
    #                                 bootImage1=self.config['Image']['flexspi_cm4_flexspi_uboot_dummy_ocram'])
    #     #set boot device then reset
    #     self.bcu.set_boot_device('flexspi')
    #     self.bcu.reset()     
    #     #clear console buffer
    #     self.com_cm4.clear_buffer()
    #     self.com_uboot.clear_buffer()
    #     #checking boot expectation
    #     self.com_uboot.find('Hit any key to stop autoboot', timeout = 5)
    #     self.com_cm4.find('hello world Flexspi', timeout = 10)

    # def test_flexspi_boot_cm4_flexspi_uboot_dummy_ddr(self):
    #     #download image
    #     self.image.download_image('test_flexspi_boot_cm4_flexspi_uboot_dummy_ddr', 'flexspi', SDPimage=self.config['Image']['serial_download'], 
    #                                 bootImage1=self.config['Image']['flexspi_cm4_flexspi_uboot_dummy_ddr'])
    #     #set boot device then reset
    #     self.bcu.set_boot_device('flexspi')
    #     self.bcu.reset()     
    #     #clear console buffer
    #     self.com_cm4.clear_buffer()
    #     self.com_uboot.clear_buffer()
    #     #checking boot expectation
    #     self.com_uboot.find('Hit any key to stop autoboot', timeout = 5)
    #     self.com_cm4.find('hello world Flexspi', timeout = 10)


    # def test_flexspi_secondary_boot_cm4_flexspi_uboot_dummy_ddr(self):
    #     #download image
    #     self.image.download_image('test_flexspi_secondary_boot_cm4_flexspi_uboot_dummy_ddr', 'flexspi', SDPimage=self.config['Image']['serial_download'], 
    #                                 bootImage2=self.config['Image']['flexspi_cm4_flexspi_uboot_dummy_ddr'])
    #     #set boot device then reset
    #     self.bcu.set_boot_device('flexspi')
    #     self.bcu.reset()     
    #     #clear console buffer
    #     self.com_cm4.clear_buffer()
    #     self.com_uboot.clear_buffer()
    #     #checking boot expectation
    #     self.com_uboot.find('Hit any key to stop autoboot', timeout = 5)
    #     self.com_cm4.find('hello world Flexspi', timeout = 10)

    # def test_flexspi_no_image_enter_sdp(self):
    #     #clear all the images from each boot device
    #     self.image.download_image('test_flexspi_no_image_enter_sdp', 'clear', SDPimage = self.config['Image']['serial_download'])
    #     #set boot device as sd then reset
    #     self.bcu.set_boot_device('flexspi')
    #     self.bcu.reset()
    #     #check if SDP can boot image successfully
    #     self.image.download_image('test_flexspi_no_image_enter_sdp', 'clear', SDPimage = self.config['Image']['serial_download'])
    #     #check boot expectation
    #     self.com_uboot.find('Detect USB boot. Will enter fastboot mode', timeout = 5)


    @pytest.mark.parametrize('par', [i for i in range(1, 8, 1)])
    def test_flexspi_boot_cm4_flexspi_uboot_single_sdr_4B_(self,par):
        image_path = os.path.join(main_path,'image','flexspi')
        output_image = os.path.join(image_path, 'test_flexspi_boot_cm4_flexspi_uboot_single_sdr_4B_{}.bin'.format(par))
        self.gen_img.generate_flexspi_image(vendor='micron', pad='single', is_ddr=0, is_32bit=1, patch_offset='0x400', freq=par, ifile=self.config['Image']['flexspi_cm4_flexspi_uboot_dummy_ddr'], ofile=output_image)
        #download image
        self.image.download_image('test_flexspi_boot_cm4_flexspi_uboot_single_sdr_4B_{}'.format(par), 'flexspi', SDPimage=self.config['Image']['serial_download'], 
                                    bootImage1=output_image)
        #set boot device then reset
        self.bcu.set_boot_device('flexspi')
        self.bcu.reset()
        #clear console buffer
        self.com_cm4.clear_buffer()
        self.com_uboot.clear_buffer()
        #checking boot expectation
        self.com_uboot.find('Hit any key to stop autoboot', timeout = 5)
        self.com_cm4.find('hello world Flexspi', timeout = 10)

    @pytest.mark.parametrize('par', [i for i in range(1, 8, 1)])
    def test_flexspi_boot_cm4_flexspi_uboot_single_sdr_3B_(self,par):
        image_path = os.path.join(main_path,'image','flexspi')
        output_image = os.path.join(image_path, 'test_flexspi_boot_cm4_flexspi_uboot_single_sdr_3B_{}.bin'.format(par))
        self.gen_img.generate_flexspi_image(vendor='micron', pad='single', is_ddr=0, is_32bit=0, patch_offset='0x400', freq=par, ifile=self.config['Image']['flexspi_cm4_flexspi_uboot_dummy_ddr'], ofile=output_image)
        #download image
        self.image.download_image('test_flexspi_boot_cm4_flexspi_uboot_single_sdr_3B_{}'.format(par), 'flexspi', SDPimage=self.config['Image']['serial_download'], 
                                    bootImage1=output_image)
        #set boot device then reset
        self.bcu.set_boot_device('flexspi')
        self.bcu.reset()
        #clear console buffer
        self.com_cm4.clear_buffer()
        self.com_uboot.clear_buffer()
        #checking boot expectation
        self.com_uboot.find('Hit any key to stop autoboot', timeout = 5)
        self.com_cm4.find('hello world Flexspi', timeout = 10)


    @pytest.mark.parametrize('par', [i for i in range(1, 8, 1)])
    def test_flexspi_boot_cm4_flexspi_uboot_octal_ddr_4B_(self,par):
        image_path = os.path.join(main_path,'image','flexspi')
        output_image = os.path.join(image_path, 'test_flexspi_boot_cm4_flexspi_uboot_octal_ddr_4B_{}.bin'.format(par))
        self.gen_img.generate_flexspi_image(vendor='micron', pad='octal', is_ddr=1, is_32bit=1, patch_offset='0x400', freq=par, ifile=self.config['Image']['flexspi_cm4_flexspi_uboot_dummy_ddr'], ofile=output_image)
        #download image
        self.image.download_image('test_flexspi_boot_cm4_flexspi_uboot_octal_ddr_4B_{}'.format(par), 'flexspi', SDPimage=self.config['Image']['serial_download'], 
                                    bootImage1=output_image)
        #set boot device then reset
        self.bcu.set_boot_device('flexspi')
        self.bcu.reset()
        #clear console buffer
        self.com_cm4.clear_buffer()
        self.com_uboot.clear_buffer()
        #checking boot expectation
        self.com_uboot.find('Hit any key to stop autoboot', timeout = 5)
        self.com_cm4.find('hello world Flexspi', timeout = 10)

    @pytest.mark.parametrize('par', [i for i in range(1, 8, 1)])
    def test_flexspi_boot_cm4_flexspi_uboot_octal_sdr_4B_(self,par):
        image_path = os.path.join(main_path,'image','flexspi')
        output_image = os.path.join(image_path, 'test_flexspi_boot_cm4_flexspi_uboot_octal_sdr_4B_{}.bin'.format(par))
        self.gen_img.generate_flexspi_image(vendor='micron', pad='octal', is_ddr=0, is_32bit=1, patch_offset='0x400', freq=par, ifile=self.config['Image']['flexspi_cm4_flexspi_uboot_dummy_ddr'], ofile=output_image)
        #download image
        self.image.download_image('test_flexspi_boot_cm4_flexspi_uboot_octal_sdr_4B_{}'.format(par), 'flexspi', SDPimage=self.config['Image']['serial_download'], 
                                    bootImage1=output_image)
        #set boot device then reset
        self.bcu.set_boot_device('flexspi')
        self.bcu.reset()
        #clear console buffer
        self.com_cm4.clear_buffer()
        self.com_uboot.clear_buffer()
        #checking boot expectation
        self.com_uboot.find('Hit any key to stop autoboot', timeout = 5)
        self.com_cm4.find('hello world Flexspi', timeout = 10)

if __name__ == '__main__':
    import subprocess
    pytest = os.path.abspath(os.path.join(sys.executable, '..', 'Scripts', 'py.test.exe'))
    cmd = ['test_flexspi_boot.py::TestFlexspiBoot::test_flexspi_boot_cm4_flexspi_uboot_single_sdr_4B_']
    subprocess.call([pytest, '-v' ,'-s', cmd])
    # pytest.main(['-v', '-s'])

