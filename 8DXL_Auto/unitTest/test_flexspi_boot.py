import pytest
import os
import sys
import logging
import Tkinter as tk

file_path = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')
main_path = os.path.abspath(os.path.join(file_path, '..')).replace('\\', '/')
sys.path.append(main_path)


from common import log
from common import serialspawn
from common import image_download
import subprocess


def messagebox():
    top = tk.Tk()
    top.mainloop()
    print '111111'

class TestFlexspiBoot:
    @pytest.fixture(autouse=True)
    def setup(self, request, cfg):
        #sall the paramaters got from config.yaml
        self.config = cfg
        self.image = image_download.ImageDownload(self.config['UUU']['path'])

        def teardown():
            pass
        request.addfinalizer(teardown)
        
    def test_flexspi_boot_image_cm4_flexspi(self):
        messagebox()
        #download image
        self.image.download_image('test_flexspi_boot_image_cm4_flexspi', device='flexspi', SDPimage=self.config['Image']['serial_download'], 
                                    bootImage1=self.config['Image']['flexspi_cm4_flexspi_uboot'])
        messagebox()
        #checking boot expectation
        spawn = serialspawn.SerialSpawn(self.config['COM']['CM4'], self.config['COM']['CM4_baudrate'])
        spawn.find('hello', timeout = 10)
        spawn.close()


    def test_flexspi_boot_image1_invalid_SECO_container_image2_uboot(self):
        messagebox()
        #download image
        self.image.download_image('test_flexspi_boot_image1_invalid_SECO_container_image2_uboot', device='flexspi', SDPimage=self.config['Image']['serial_download'], 
                                    bootImage1 = self.config['Image']['flexspi_invalid_scfw_entity'], bootImage2=self.config['Image']['flexspi_cm4_flexspi_uboot'])
        messagebox()
        #checking boot expectation
        spawn = serialspawn.SerialSpawn(self.config['COM']['uBoot'], self.config['COM']['uBoot_baudrate'])
        spawn.find('Hit any key to stop autoboot', timeout = 5)
        spawn.close()


if __name__ == '__main__':
      # pytest.main(['-v', '-s'])
    # import subprocess
    pytest = os.path.abspath(os.path.join(sys.executable, '..', 'Scripts', 'py.test.exe'))
    cmd = ['test_flexspi_boot.py::TestFlexspiBoot::test_flexspi_boot_image1_invalid_SECO_container_image2_uboot']
    subprocess.call([pytest, '-v' ,'-s', cmd])
    # pytest.main(['-v', '-s'])

